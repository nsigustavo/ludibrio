"""
This module provides doctest compatibility for Python < 3.
"""
import sys


if sys.version_info < (3,):
    # Python 2 doesn't include the exception's module name in tracebacks, but
    # Python 3 does. Simulate this for doctests by setting __name__ to the
    # exception's fully-qualified name.
    from ludibrio.matcher import ParameterException
    from ludibrio.mock import MockExpectationError
    from ludibrio.spy import SpyExpectationError
    ParameterException.__name__ = 'ludibrio.matcher.ParameterException'
    MockExpectationError.__name__ = 'ludibrio.mock.MockExpectationError'
    SpyExpectationError.__name__ = 'ludibrio.spy.SpyExpectationError'
