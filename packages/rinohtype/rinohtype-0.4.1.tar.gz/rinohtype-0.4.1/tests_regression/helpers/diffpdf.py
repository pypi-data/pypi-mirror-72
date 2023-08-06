#! /usr/bin/env python

# usage: diffpdf.py file1.pdf file2.pdf

# requirements:
# - ImageMagick (convert)
# - MuPDF's mutool >= 1.13.0
#   or poppler's pdftoppm (known to work: 0.18.4, 0.41.0, 0.85.0, 0.89.0;
#                          known to fail: 0.42.0)

import os
import shutil
import sys

from decimal import Decimal
from functools import partial
from multiprocessing import Pool, cpu_count
from shutil import which
from subprocess import Popen, PIPE, DEVNULL

from rinoh.backend.pdf import PDFReader


DIFF_DIR = 'pdfdiff'
SHELL = sys.platform == 'win32'


def diff_pdf(a_filename, b_filename):
    a_pages = PDFReader(a_filename).catalog['Pages']['Count']
    b_pages = PDFReader(b_filename).catalog['Pages']['Count']

    success = True
    if a_pages != b_pages:
        print('PDF files have different lengths ({} and {})'
              .format(a_pages, b_pages))
        success = False

    if os.path.exists(DIFF_DIR):
        for item in os.listdir(DIFF_DIR):
            item_path = os.path.join(DIFF_DIR, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    else:
        os.mkdir(DIFF_DIR)

    min_pages = min(a_pages, b_pages)
    page_numbers = list(range(1, min_pages + 1))
    # https://pymotw.com/2/multiprocessing/communication.html#process-pools
    pool_size = cpu_count()
    pool = Pool(processes=pool_size)
    print('Running {} processes in parallel'.format(pool_size))
    perform_diff = partial(diff_page, a_filename, b_filename)
    try:
        pool_outputs = pool.map(perform_diff, page_numbers)
    except CommandFailed as exc:
        raise SystemExit('Problem running mutool/pdftoppm'
                         ' or convert (page {})!'.format(exc.page_number))
    pool.close() # no more tasks
    pool.join()  # wrap up current tasks

    for page_number, page_diff in zip(page_numbers, pool_outputs):
        if page_diff != 0:
            print('page {} ({})'.format(page_number, page_diff))
            success = False
    return success


class CommandFailed(Exception):
    def __init__(self, page_number):
        self.page_number = page_number


def diff_page(a_filename, b_filename, page_number):
    if compare_page(a_filename, b_filename, page_number):
        return 0

    diff_jpg_path = os.path.join(DIFF_DIR, '{}.jpg'.format(page_number))
    # http://stackoverflow.com/a/28779982/438249
    diff = Popen(['convert', '-', '(', '-clone', '0-1', '-compose', 'darken',
                                       '-composite', ')',
                  '-channel', 'RGB', '-combine', diff_jpg_path],
                 shell=SHELL, stdin=PIPE)
    a_page = pdf_page_to_ppm(a_filename, page_number, diff.stdin, gray=True)
    if a_page.wait() != 0:
        raise CommandFailed(page_number)
    b_page = pdf_page_to_ppm(b_filename, page_number, diff.stdin, gray=True)
    diff.stdin.close()
    if b_page.wait() != 0 or diff.wait() != 0:
        raise CommandFailed(page_number)
    grayscale = Popen(['convert', diff_jpg_path, '-colorspace', 'HSL',
                       '-channel', 'g', '-separate', '+channel', '-format',
                       '%[fx:mean]', 'info:'], shell=SHELL, stdout=PIPE)
    return Decimal(grayscale.stdout.read().decode('ascii'))


def compare_page(a_filename, b_filename, page_number):
    """Returns ``True`` if the pages at ``page_number`` are identical"""
    compare = Popen(['compare', '-', '-metric', 'AE', 'null:'],
                    shell=SHELL, stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL)
    a_page = pdf_page_to_ppm(a_filename, page_number, compare.stdin)
    if a_page.wait() != 0:
        raise CommandFailed(page_number)
    b_page = pdf_page_to_ppm(b_filename, page_number, compare.stdin)
    compare.stdin.close()
    if b_page.wait() != 0:
        raise CommandFailed(page_number)
    return compare.wait() == 0


def pdftoppm(pdf_path, page_number, stdout, gray=False):
    command = ['pdftoppm', '-f', str(page_number),
               '-singlefile', str(pdf_path)]
    if gray:
        command.insert(-1, '-gray')
    return Popen(command, shell=SHELL, stdout=stdout)


def mutool(pdf_path, page_number, stdout, gray=False):
    command = ['mutool', 'draw', '-r', '150', '-F', 'ppm', '-o', '-',
               str(pdf_path), str(page_number)]
    if gray:
        command.insert(-2, '-c')
        command.insert(-2, 'gray')
    return Popen(command, shell=SHELL, stdout=stdout)


if which('mutool'):
    pdf_page_to_ppm = mutool
elif which('pdftoppm'):
    pdf_page_to_ppm = pdftoppm
else:
    print("mutool or poppler's pdftoppm is required", file=sys.stderr)
    raise SystemExit(2)


if __name__ == '__main__':
    _, a_filename, b_filename = sys.argv
    rc = 0 if diff_pdf(a_filename, b_filename) else 1
    raise SystemExit(rc)
