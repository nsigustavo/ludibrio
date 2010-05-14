#-*- coding:utf-8 -*-

from inspect import getframeinfo
from sys import _getframe as getframe
from _testdouble import _TestDouble

STOPRECORD = False
RECORDING = True

class Stub(_TestDouble):
    """Stubs provides canned answers to calls made during the test.
    """
    __expectation__= [] # [(attribute, args, kargs),]
    __recording__ = RECORDING
    __lastPropertyCalled__ = None

    def __enter__(self):
        self.__expectation__= []
        self.__recording__ = RECORDING
        return self

    def __methodCalled__(self, *args, **kargs):
        property_name = self.__propertyCalledName__()
        return self.__propertyCalled(property_name, args, kargs)

    def __propertyCalledName__(self):
        propertyCalledName =  self.__lastPropertyCalled__ or getframeinfo(getframe(2))[2]
        self.__lastPropertyCalled__ = None
        return propertyCalledName

    def __propertyCalled(self, property, args=[], kargs={}, response=None):
        if self.__recording__:
            self.__newExpectation([property, args, kargs, response])
            return self
        else:
            return self._expectationValue(property, args, kargs)

    def __exit__(self, type, value, traceback):
        self.__recording__ = STOPRECORD

    def __setattr__(self, attr, value):
        if attr in dir(Stub):
            object.__setattr__(self, attr, value)
        else:
            self.__propertyCalled('__setattr__', args=[attr, value])

    def __newExpectation(self, attr):
        self.__expectation__.append(attr)

    def __rshift__(self, response):
            self.__expectation__[-1][3] = response
    __lshift__ = __rshift__

    def _expectationValue(self, attr, args=[], kargs={}):
        for position, (attrExpectation, argsExpectation, kargsExpectation, response) in enumerate(self.__expectation__):
            if (attrExpectation, argsExpectation, kargsExpectation) == (attr, args, kargs):
                self.__toTheEnd__(position)
                return response
        raise AttributeError("Stub Object received unexpected call")

    def __toTheEnd__(self, position):
        self.__expectation__.append(self.__expectation__.pop(position))

    def __getattr__(self, x):
        self.__lastPropertyCalled__ = x
        return self.__propertyCalled('__getattribute__', (x,), response=self)
