from __future__ import with_statement
import doctest
print doctest.testfile("../README",
                       optionflags=doctest.REPORT_ONLY_FIRST_FAILURE + doctest.ELLIPSIS,
                       globs=globals())
