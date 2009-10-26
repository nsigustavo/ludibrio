#python:_testludibrio.py
from __future__ import with_statement
import doctest
#print doctest.testfile("../README",
#                       optionflags=doctest.REPORT_ONLY_FIRST_FAILURE + doctest.ELLIPSIS,
#                       globs=globals())

import unittest
import doctest


def _test():
    return doctest.testfile("../README", optionflags=doctest.REPORT_ONLY_FIRST_FAILURE + doctest.ELLIPSIS, globs=globals())

if __name__ == '__main__':
    print _test()

