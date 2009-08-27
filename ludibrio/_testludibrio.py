import doctest
import ludibrio
import __future__
import doctest


#adiciona flags ao doctest para __future__ with_statement
_extract_future_flags_old = doctest._extract_future_flags
def _extract_future_flags(globs):
        flags = _extract_future_flags_old(globs)
        flags = flags +__future__.with_statement.compiler_flag
        return flags
doctest._extract_future_flags = _extract_future_flags


print doctest.testfile("../README", optionflags=doctest.REPORT_ONLY_FIRST_FAILURE + doctest.ELLIPSIS  +__future__.with_statement.compiler_flag)

