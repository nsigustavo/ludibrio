from helpers import frameOutOfContext
from inspect import getframeinfo, getmodule
from sys import _getframe
from types import ModuleType
import gc

_oldimport = __import__


class DependencyInjection(object):

    def __enter__(self):
        __builtins__['__import__'] = self.import_double
        return self

    def __exit__(self, type, value, traceback):
        __builtins__['__import__'] = _oldimport
    
    def import_double(self, name, globals={}, locals={}, fromlist=[], level=-1):
        """import_double(name, globals={}, locals={}, fromlist=[], level=-1) -> module
        """
        if not fromlist:raise ImportError('Use: from ... import ...')
        module = _oldimport(name, globals, locals, fromlist, level)
        self.original = module.__dict__[fromlist[0]]
        self.frame = frameOutOfContext()
        return module

    def inject(self, double):
        self.double = double
        self._original_to_double()
    
    def restoure_import(self):
        self._double_to_original()

    def _original_to_double(self):
        self._replace_all(self.original, self.double)

    def _double_to_original(self):
        self._replace_all(self.double, self.original)

    def _replace_all(self, old, new):
        self._old, self._new = old, new
        self._replace_in_context(self.frame.f_locals)
        for module in self._all_modules():
            self._replace_in_context(module.__dict__)

    def _replace_in_context(self, context_dict):
         for k, v in context_dict.items():
                if v is self._old:
                    context_dict[k] = self._new
    
    def _all_modules(self):
        for obj in gc.get_objects():
            if isinstance(obj, ModuleType):
                yield obj
