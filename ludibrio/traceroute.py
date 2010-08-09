from inspect import getframeinfo, getmodule
from sys import _getframe
import traceback
from ludibrio._testdouble import _TestDouble
from helpers import frame_out_of_context

class TraceRoute(_TestDouble):
    def __init__(self):
        self.__traceback__= []

    def remember(self):
        frame = self._frame_of_trace()
        traceinfo = getframeinfo(frame)
        if self._is_equal_to_last(traceinfo):
            self.__traceback__.append(traceinfo)

    def _is_equal_to_last(self, trace):
        return bool(not self.__traceback__
                    or not self.__traceback__[-1].filename == trace.filename
                    or not self.__traceback__[-1].lineno == trace.lineno)

    def _frame_of_trace(self):
        return frame_out_of_context()

    def stack_trace(self, limit=10):
        """Format a stack trace and return."""
        return 'Stack trace (most recent call last)\n''  '+''.join(
                    traceback.format_list(self._extracted_list()[:limit])
                    ).strip()

    def _extracted_list(self):
        """return a list of strings ready for printing."""
        return [[route.filename,
                 route.lineno,
                 route.function,
                 self._format_code_context(route.code_context)]
                     for route in self.__traceback__]


    def stack_code(self, limit=10):
        return '\n'.join(
                [self._format_code_context(route.code_context)
                    for route in self.__traceback__[:limit]])

    def _format_code_context(self, code_context):
        return '\n'.join([line.strip() for line in code_context])

    def most_recent_call(self):
        last_code = self.__traceback__[-1].code_context
        return self._format_code_context(last_code)

    def __methodCalled__(self, *args, **kargs):
        self.remember()
        return self

    def __iter__(self):
        self.remember()
        yield self

    def __str__(self):
        self.remember()
        return self.__kargs__.get('str', 'TraceRoute Object')

    def __int__(self):
        self.remember()
        return self.__kargs__.get('int', 1)

    def __float__(self):
        self.remember()
        return self.__kargs__.get('float', 1.0)

    def __nonzero__(self):
        self.remember()
        return True

    def __getattr__(self, x):
        self.remember()
        return self

