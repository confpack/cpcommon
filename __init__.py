from __future__ import print_function, absolute_import

from contextlib import contextmanager
import os
import os.path
import sys

from .cmdline import Command


def verify_file_exists_or_sysexit(path, argparser=None):
  if not os.path.isfile(path):
    print("error: {} is not a valid file".format(path), file=sys.stderr)
    if argparser:
      argparser.print_help()

    sys.exit(1)


def verify_directory_exists_or_sysexit(path, argparser=None):
  if not os.path.isdir(path):
    print("error: {} is not a valid directory".format(path), file=sys.stderr)
    if argparser:
      argparser.print_help()

    sys.exit(1)


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as e:
    if e.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else:
      raise
