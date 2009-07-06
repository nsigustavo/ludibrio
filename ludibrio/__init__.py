#-*- coding:utf-8 -*-
"""
MOCK
====
Mocks are what we are talking about here:
objects pre-programmed with expectations which form a
specification of the calls they are expected to receive.

>>> with mock() as greetings:
...     greetings.excuse_me() >> 'Com licença'
...     greetings.hello('Gustavo') >> 'Ola, Gustavo'
...     greetings.see_you_soon >> 'Até logo'
...     greetings.see_you_soon >> 'Até logo, denovo'

>>> print greetings.excuse_me()
Com licença

>>> print greetings.hello('Gustavo')
Ola, Gustavo

>>> print greetings.see_you_soon
Até logo

>>> print greetings.see_you_soon
Até logo, denovo


>>> print greetings.see_you_soon
Traceback (most recent call last):
...
AssertionError: Object's mocks are not pre-programmed with expectations:see_you_soon


>>> with mock() as greetings:
...     greetings.excuse_me() >> 'Com licença'
...     greetings.see_you_soon >> 'Até logo'

>>> print greetings.excuse_me()
Com licença

>>> print greetings.hello('Gustavo')
Traceback (most recent call last):
...
AssertionError: Object's mocks are not pre-programmed with expectations:hello


Stubs
=====
Stubs provide canned answers to calls made during the test,
usually not responding at all to anything outside what's programmed in for the test.

>>> with stub() as greetings:
...     greetings.excuse_me() >> 'Com licença'
...     greetings.hello('Gustavo') >> 'Ola, Gustavo'
...     greetings.see_you_soon = 'Até logo'


>>> print greetings.hello('Gustavo')
Ola, Gustavo

>>> print greetings.excuse_me()
Com licença

>>> print greetings.hello('Gustavo')
Ola, Gustavo

>>> print greetings.see_you_soon
Até logo


Dummy
=====
Dummy objects are passed around but never validated.


>>> Dummy()
Dummy object

>>> def teste(x):
...     x.write("teste")
...     x.close()

>>> teste(Dummy()) #Dummy ~== Foda-se

>>> dummy = Dummy()
>>> dummy.foo()
Dummy object
>>> dummy.bar
Dummy object
>>> dummy.one.two.three()
Dummy object

>>> 1 + Dummy()
Dummy object
>>> Dummy() -1
Dummy object
>>> Dummy()[4]
Dummy object

>>> dummy = Dummy()
>>> dummy ** 22 and dummy / dummy
Dummy object
>>> dummy * 69 or dummy // dummy == "Anything"
Dummy object

>>> for i in Dummy():print i
Dummy object

>>> list(Dummy())
[Dummy object]
>>> Dummy()[2:9]
Dummy object
"""

from __future__ import with_statement
from contextlib import contextmanager

STOPCREATION = False
CREATION = True


class Dummy(object):
    """Dummy objects are passed around, but never validated.
    """
    def __getattr__(self, x):
        return Dummy()
    def __init__(self, *args, **kargs):
        pass

    def __call__(self, *args, **kargs):
        return Dummy()

    def __iter__(self):
        yield Dummy()

    def __str__(self):
        return "Dummy object"

    __repr__ = __str__

    def __nonzero__(self):
        return True

    __item__ = __int__ = __contains__ = __eq__ = __ge__ = __getitem__ =\
    __gt__ = __le__ = __len__ = __lt__ = __ne__ = __setitem__ =        \
    __delattr__ = __delitem__ = __add__ = __and__ = __delattr__ =      \
    __div__ = __divmod__ = __float__ = __floordiv__ = __invert__ =     \
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
    __status__ = CREATION

    def __exit__(self):
        self.__status__ = STOPCREATION
        for name, value in self.__properties__.items():
            value.__exit__()

    def  __getattr__(self, attr):
        if attr.startswith("__") and not self.__status__ is CREATION:
            raise AttributeError, (
            "type object '%s' has no attribute '%s'") %(
                                    self.__name__, attr)
        if attr in self.__properties__.keys():
            return self.__properties__[attr]
        ob_attr = Attribute()
        self.__properties__[attr]=ob_attr
        return ob_attr


class Attribute(object):
    args = []
    __status__ = CREATION
    kargs = {}
    result = None
    property = True

    def __call__(self, *args, **kargs):
        if self.__status__ == CREATION:
            self.property = False
            self.args = args
            self.kargs = kargs
            return self
        else:
            return self.result

    def __rshift__(self, result):
        self.result = result

    def __exit__(self):
        self.__status__ = STOPCREATION

@contextmanager
def stub():
    stub_obj=Stub()
    yield stub_obj
    stub_obj.__exit__()


class Mock(object):
    """Mocks are what we are talking about here:
    objects pre-programmed with expectations which form a
    specification of the calls they are expected to receive.
    """
    #TODO: mock  __getitem__ == []
    #TODO: mock + - * / ...
    __status__ = CREATION
    __expectations__ = []

    def __getattr__(self, attr):
        if  attr.startswith("__"):
            return self.__getMockAttr(self, attr)
        else:
            if self.__status__ is CREATION:
                return self.__getMockAttrCreation(attr)
            else:
                return self.__getMockedAttrExpectation(attr)

    def __getMockedAttrExpectation(self, attr):
        if (not self.__expectations__
           or not self.__expectations__[-1][0] == attr):
            self.__error("%s"%(attr))
        else:
            ob = self.__expectations__.pop()[1]
            return ob.result if ob.property else ob

    def __getMockAttrCreation(self, attr):
        ob_attr = Attribute()
        self.__expectations__ = (
            [(attr,ob_attr)] + self.__expectations__)
        return ob_attr

    def __getMockAttr(self, attr):
        return object.__getattr__(self, attr)

    def __rshift__(self, result):
        self.result = result

    def __setattr__(self, attr, value):
        if attr.startswith("__"):
            self.__setMockAttr(attr, value)
        else:
            if self.__status__ is CREATION:
                self.__setMockAttrCreation(attr, value)
            else:
                self.__setMockedAttrExpectation(attr, value)

    def __setMockedAttrExpectation(self, attr, value):
        if (not len(self.__expectations__)>=0
           or not self.__expectations__.pop() == (attr, value)):
            self.__error("%s = %s"%( attr, value))

    def __setMockAttrCreation(self, attr, value):
        self.__expectations__ = (
            [(attr, value)] + self.__expectations__)

    def __setMockAttr(self, attr, value):
        object.__setattr__(self, attr, value)

    def __error(self, call):
        raise AssertionError , (
        "Object's mocks are not pre-programmed with expectations:%s")%(
        call)

    def __exit__(self):
        self.__status__ = STOPCREATION
        for attr, value in self.__expectations__:
            if isinstance(value, Attribute):
                value.__exit__()


@contextmanager
def mock():
    mock_obj=Mock()
    yield mock_obj
    mock_obj.__exit__()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
