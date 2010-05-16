from inspect import getframeinfo, getmodule
from sys import _getframe
import traceback
from _testdouble import _TestDouble


class TraceRoute(_TestDouble):
    __traceback__= []
    
    def remember(self):
        frame = self._getFrameOfTrace()
        traceinfo = getframeinfo(frame)
        if self._isEqualToLast(traceinfo):
            self.__traceback__.append(traceinfo)

    def _isEqualToLast(self, trace):
        return bool(not self.__traceback__
                    or not self.__traceback__[-1].filename == trace.filename
                    or not self.__traceback__[-1].lineno == trace.lineno)
            
    def _getFrameOfTrace(self):
        this_frame = frame = _getframe(0)
        while 'ludibrio' in frame.f_code.co_filename:
            frame = frame.f_back
        return frame

    def stackTrace(self, limit=10):
        """Format a stack trace and return."""
        return 'Stack trace (most recent call last)\n''  '+''.join(
                    traceback.format_list(self._extracted_list()[:limit])
                    ).strip()

    def _extracted_list(self):
        """return a list of strings ready for printing."""
        return [[route.filename,
                 route.lineno,
                 route.function,
                 self._formatCodeContext(route.code_context)]
                     for route in self.__traceback__]
             

    def stackCode(self, limit=10):
        return '\n'.join(
                [self._formatCodeContext(route.code_context)
                    for route in self.__traceback__[:limit]])
    
    def _formatCodeContext(self, code_context):
        return '\n'.join([line.strip() for line in code_context]) 
    
    def mostRecentCall(self):
        last_code = self.__traceback__[-1].code_context
        return self._formatCodeContext(last_code)    
    
    def __methodCalled__(self, *args, **kargs):
        self.remember()
        return self

    def __iter__(self):
        self.remember()
        yield self

    def __str__(self):
        self.remember()
        return self.__kargs__.get('str', 'Dummy Object')

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

