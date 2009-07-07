#-*- coding:utf-8 -*-
"""
Workflow basico de criacao dos objetos (Mock, Stub)
    class controlled_execution:
        def __enter__(self):
            set things up "RECORDING"
            return thing
        def __exit__(self, type, value, traceback):
            tear things down "STOPRECORD"

    with controlled_execution() as thing:
         RECORD

"""
from __future__ import with_statement
from inspect import getframeinfo
from sys import _getframe as getframe
STOPRECORD = False
RECORDING = True


class Dummy(object):
    """Dummy objects are passed around, but never validated.
    """

    def __init__(self, *args, **kargs):
        pass

    def __getattr__(self, x):
        return Dummy()

    def __call__(self, *args, **kargs):
        return Dummy()

    def __iter__(self):
        yield Dummy()

    def __str__(self):
        return 'Dummy object'

    def __int__(self):
        return 1

    def __float__(self):
        return 1.0

    __repr__ = __str__

    def __nonzero__(self):
        return True

    __item__ = __contains__ = __eq__ = __ge__ = __getitem__ =          \
    __gt__ = __le__ = __len__ = __lt__ = __ne__ = __setitem__ =        \
    __delattr__ = __delitem__ = __add__ = __and__ = __delattr__ =      \
    __div__ = __divmod__ = __floordiv__ = __invert__ =                 \
    __long__ = __lshift__ = __mod__ = __mul__ = __neg__ = __or__ =     \
    __pos__ = __pow__ = __radd__ = __rand__ = __rdiv__ = __rfloordiv__=\
    __rlshift__ = __rmod__ = __rmul__ = __ror__ = __rrshift__ =        \
    __rshift__ = __rsub__ = __rtruediv__ = __rxor__ = __setattr__ =    \
    __sizeof__ = __sub__ = __truediv__ = __xor__ = __call__


class Stub(object):
    """Stubs provide canned answers to calls made during the test,
    usually not responding at all to anything outside what's programmed
    in for the test.
    """
    __properties__ = {}

    def __enter__(self):
        self.__recording__ = RECORDING
        return self

    def  __getattr__(self, attr):
        if attr.startswith("__") and not self.__recording__:
            raise AttributeError, (
            "type object '%s' has no attribute '%s'") %(
                                    self.__name__, attr)
        if attr in self.__properties__.keys():
            return self.__properties__[attr]
        ob_attr = Attribute()
        self.__properties__[attr]=ob_attr
        return ob_attr

    def __exit__(self, type, value, traceback):
        if type is not None:
            raise RuntimeError("Don't Create False Expectations: %s"
                %str(value))
        self.__recording__ = STOPRECORD
        for name, value in self.__properties__.items():
            value.__exit__()


class Attribute(object):
    _args = []
    __recording__ = RECORDING
    _kargs = {}
    result = None
    property = True

    def __call__(self, *args, **kargs):
        if self.__recording__ == RECORDING:
            self.property = False
            self._args = args
            self._kargs = kargs
            return self
        else:
            return self.result

    def __rshift__(self, result):
        self.result = result

    def __exit__(self):
        self.__recording__ = STOPRECORD


class Mock(object):
    """Mocks are what we are talking about here:
    objects pre-programmed with expectations which form a
    specification of the calls they are expected to receive.
    """
    __expectations__ = []
    #TODO: mock  __getitem__ == []
    #TODO: mock + - * / ...

    def __enter__(self):
        self.__recording__ = RECORDING
        return self

    def __getattr__(self, attr):
        if  attr.startswith("__") and attr.endswith("__"):
            return self.__getBaseAttr(attr)
        else:
            if self.__recording__:
                return self.__getMockAttrCreating(attr)
            else:
                return self.__getMockedAttrExpectation(attr)

    def __setattr__(self, attr, value):
        if attr.startswith("__") and attr.endswith("__"):
            self.__setBaseAttr(attr, value)
        else:
            if self.__recording__:
                self.__setMockAttrCreating(attr, value)
            else:
                self.__setMockedAttrExpectation(attr, value)

    def __call__(self, *args, **kargs):
            functionCalled = getframeinfo(getframe(0)).function # functionCalled == __call__ or alias
            if self.__recording__:
                return self.__getMockAttrCreating(functionCalled)( *args, **kargs)
            else:
                return self.__getMockedAttrExpectation(functionCalled)( *args, **kargs)

    __item__ = __contains__ = __eq__ = __ge__ = __getitem__ = __xor__ =\
    __gt__ = __le__ = __len__ = __lt__ = __ne__ = __setitem__ =        \
    __delattr__ = __delitem__ = __add__ = __and__ = __delattr__ =      \
    __div__ = __divmod__ = __floordiv__ = __invert__ = __sub__ =       \
    __long__ = __lshift__ = __mod__ = __mul__ = __neg__ = __or__ =     \
    __pos__ = __pow__ = __radd__ = __rand__ = __rdiv__ = __rfloordiv__=\
    __rlshift__ = __rmod__ = __rmul__ = __ror__ = __rrshift__ =        \
    __rshift__ = __rsub__ = __rtruediv__ = __rxor__ =  __sizeof__ =    \
     __truediv__ = __call__

    def __rshift__(self, result):
        self.result = result

    def __exit__(self, type, value, traceback):
        if type is not None:
            raise RuntimeError("Don't Create False Expectations: %s"
                %str(value))
        self.__recording__ = STOPRECORD
        for attr, value in self.__expectations__:
            if isinstance(value, Attribute):
                value.__exit__()



    def __getMockedAttrExpectation(self, attr):
        if (not self.__expectations__
           or not self.__expectations__[-1][0] == attr):
            self.__error("%s"%(attr))
        else:
            ob = self.__expectations__.pop()[1]
            return ob.result if ob.property else ob

    def __getMockAttrCreating(self, attr):
        ob_attr = Attribute()
        self.__expectations__ = (
            [(attr,ob_attr)] + self.__expectations__)
        return ob_attr

    def __getBaseAttr(self, attr):
        return object.__getattribute__(self, attr)

    def __setMockedAttrExpectation(self, attr, value):
        if (not len(self.__expectations__)>=0
           or not self.__expectations__.pop() == (attr, value)):
            self.__error("%s = %s"%( attr, value))

    def __setMockAttrCreating(self, attr, value):
        self.__expectations__ = (
            [(attr, value)] + self.__expectations__)

    def __setBaseAttr(self, attr, value):
        object.__setattr__(self, attr, value)

    def __error(self, call):
        raise AssertionError , (
        "Object's mocks are not pre-programmed with expectations:%s")%(
        call)
