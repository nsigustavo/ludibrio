#-*- coding:utf-8 -*-

from inspect import getframeinfo
from sys import _getframe as getframe
from _testdouble import _TestDouble
from dependencyinjection import DependencyInjection
from traceroute import TraceRoute
from ludibrio.helpers import format_called

STOPRECORD = False
RECORDING = True


class Stub(_TestDouble):
    """Stubs provides canned answers to calls made during the test.
    """
    __expectation__= [] # [(attribute, args, kargs),]
    __recording__ = RECORDING
    __lastPropertyCalled__ = None
    __dependency_injection__ = None
    __traceroute__ = None

    def __enter__(self):
        self.__expectation__= []
        self.__traceroute__ = TraceRoute()
        self.__recording__ = RECORDING
        self.__dependency_injection__ = DependencyInjection(double = self)
        return self

    def __methodCalled__(self, *args, **kargs):
        property_name = self._property_called_name()
        return self._property_called(property_name, args, kargs)

    def _property_called_name(self):
        propertyCalledName =  self.__lastPropertyCalled__ or getframeinfo(getframe(2))[2]
        self.__lastPropertyCalled__ = None
        return propertyCalledName

    def _property_called(self, property, args=[], kargs={}, response=None):
        if self.__recording__:
            response = response if response is not None else self
            self._new_expectation([property, args, kargs, response])
            return self
        else:
            self.__traceroute__.remember()
            return self._expectation_value(property, args, kargs)

    def __exit__(self, type, value, traceback):
        self.__dependency_injection__.restoure_import()
        self.__recording__ = STOPRECORD

    def __setattr__(self, attr, value):
        if attr in dir(Stub):
            object.__setattr__(self, attr, value)
        else:
            self._property_called('__setattr__', args=[attr, value])

    def _new_expectation(self, attr):
        self.__expectation__.append(attr)

    def __rshift__(self, response):
            self.__expectation__[-1][3] = response
    __lshift__ = __rshift__

    def _expectation_value(self, attr, args=[], kargs={}):
        for position, (attrExpectation, argsExpectation, kargsExpectation, response) in enumerate(self.__expectation__):
            if (attrExpectation, argsExpectation, kargsExpectation) == (attr, args, kargs):
                self._to_the_end(position)
                return response
        if self.__kargs__.has_key('proxy'):
            return getattr(self.__kargs__.get('proxy'), attr)(*args, **kargs)
        raise AttributeError(
            "Stub Object received unexpected call. %s\n%s"%(
                    self.format_called(attr, args, kargs),
                    self.__traceroute__.stack_trace()))

    def format_called(self, attr, args, kargs):
        if attr == '__call__' and self.__lastPropertyCalled__:
            attr = self.__lastPropertyCalled__
        return format_called(attr, args, kargs)

    def _to_the_end(self, position):
        self.__expectation__.append(self.__expectation__.pop(position))

    def __getattr__(self, x):
        self.__lastPropertyCalled__ = x
        return self._property_called('__getattribute__', (x,), response=self)
    
    def __del__(self):
        self.__dependency_injection__.restoure_object()
    
    def restoure_import(self):
        self.__dependency_injection__.restoure_object()
