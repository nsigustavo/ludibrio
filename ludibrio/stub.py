#-*- coding:utf-8 -*-

from inspect import getframeinfo
from sys import _getframe as getframe
from _testdouble import _ProxyToAlias
from dependencyinjection import DependencyInjection
from traceroute import TraceRoute
from ludibrio.helpers import format_called

STOPRECORD = False
RECORDING = True


class Stub(_ProxyToAlias):
    """Stubs provides canned answers to calls made during the test.
    """
    __expectation__= [] # [(attribute, args, kargs),]
    __recording__ = RECORDING
    __last_property_called__ = None
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
        property_called_name =  self.__last_property_called__ or getframeinfo(getframe(2))[2]
        self.__last_property_called__ = None
        return property_called_name

    def _property_called(self, property, args=[], kargs={}, response=None):
        if self.__recording__:
            response = response if response is not None else self
            self._new_expectation([property, args, kargs, response])
            return self
        else:
            self.__traceroute__.remember()
            return self._expectation_value(property, args, kargs)

    def __exit__(self, type, value, traceback):
        self.__dependency_injection__.restore_import()
        self.__recording__ = STOPRECORD

    def __setattr__(self, attr, value):
        if attr in dir(Stub):
            object.__setattr__(self, attr, value)
        else:
            self._property_called('__setattr__', args=[attr, value])

    def _new_expectation(self, expectation):
        self.__expectation__.append(expectation)

    def __rshift__(self, response):
            self.__expectation__[-1][3] = response
    gives = __lshift__ = __rshift__

    def _expectation_value(self, attr, args=[], kargs={}):
        for position, (attr_expectation, args_expectation, kargs_expectation, response) in enumerate(self.__expectation__):
            if (attr_expectation, args_expectation, kargs_expectation) == (attr, args, kargs):
                self._to_the_end(position)
                if isinstance(response, Exception):
	                raise response
                else:
	                return response 
        if self._has_proxy():
            return self._proxy(attr, args, kargs)
        self._attribute_expectation(attr, args, kargs)

    def _attribute_expectation(self, attr, args, kargs):
        raise AttributeError(
            "\n%s\nStub Object received unexpected call: %s"%(
                    self.__traceroute__.stack_trace(),
                    self._format_called(attr, args, kargs),
					))

    def _proxy(self, attr, args, kargs):
        return getattr(self.__kargs__.get('proxy'), attr)(*args, **kargs)

    def _has_proxy(self):
        return self.__kargs__.has_key('proxy')

    def _format_called(self, attr, args, kargs):
        if attr == '__call__' and self.__last_property_called__:
            attr = self.__last_property_called__
        return format_called(attr, args, kargs)

    def _to_the_end(self, position):
        self.__expectation__.append(self.__expectation__.pop(position))

    def __getattr__(self, x):
        self.__last_property_called__ = x
        return self._property_called('__getattribute__', (x,), response=self)
    
    def __del__(self):
        self.__dependency_injection__.restore_object()
    
    def restore_import(self):
        self.__dependency_injection__.restore_object()
