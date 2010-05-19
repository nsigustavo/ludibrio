#-*- coding:utf-8 -*-

#TODO: mockar imports respeitando o escopo com frame, pode-se subistituir o importe e validar a acall
#TODO: Spy ainda esta como protótipo

from __future__ import with_statement 
from inspect import getframeinfo 
from sys import _getframe as getframe 
from types import MethodType, UnboundMethodType, FunctionType 
from _testdouble import _TestDouble 
from traceroute import TraceRoute
from dependencyinjection import DependencyInjection


funcsType = [MethodType, UnboundMethodType, FunctionType]

STOPRECORD = False 
RECORDING = True 


class Mock(_TestDouble):
    """Mocks are what we are talking about here:
    objects pre-programmed with expectations which form a
    specification of the calls they are expected to receive.
    """
    __expectation__ =[]#[MockedCall(attribute, args, kargs),]
    __recording__ = RECORDING 
    __traceroute__ = None
    __traceroute_expected__ = None
    __dependency_injection__ = None

    def __enter__(self):
        self.__traceroute__ = TraceRoute()
        self.__traceroute_expected__ = TraceRoute()
        self.__expectation__ = []
        self.__recording__ = RECORDING
        self.__dependency_injection__ = DependencyInjection(double = self)
        return self

    def __methodCalled__(self, *args, **kargs):
        property = getframeinfo(getframe(1))[2]
        return self._property_called(property, args, kargs)

    def _property_called(self, property, args=[], kargs={}):
        if self.__recording__:
            self.__traceroute_expected__.remember()
            self._new_expectation(MockedCall(property, args = args, kargs = kargs, response = self))
            return self 
        else:
            self.__traceroute__.remember()
            return self._expectancy_recorded(property, args, kargs)

    def __exit__(self, type, value, traceback):
        self.__dependency_injection__.restoure_import()
        self.__recording__ = STOPRECORD

    def __setattr__(self, attr, value):
        if attr in dir(Mock):
            object.__setattr__(self, attr, value)
        else:
            self._property_called('__setattr__', args=[attr, value])

    def _new_expectation(self, attr):
        self.__expectation__.append(attr)

    def __rshift__(self, response):
            self.__expectation__[-1].setResponse(response)
    __lshift__ = __rshift__ 

    def _expectancy_recorded(self, attr, args=[], kargs={}):
        try:
            callMockada = self.__expectation__.pop(0)
            return callMockada.call(attr, args, kargs)
        except IndexError:
            raise MockExpectationError(
                  "Mock Object received unexpected call: %s" % 
                    self.__traceroute__.mostRecentCall())
        except MockCallError:
            raise MockExpectationError(
                  "Mock Object received unexpected call:\n"
                  "Expected:\n%s\n"
                  "Got:\n%s" % (
                    self.__traceroute_expected__.stackCode(),
                    self.__traceroute__.stackTrace())
                    )

    def __getattr__(self, x):
        return self._property_called('__getattribute__',[x])

    def validate(self):
        if self.__expectation__:
            raise MockExpectationError(
                    self._call_waiting_msg())

    def __del__(self):
        self.__dependency_injection__.restoure_import()
        self.__dependency_injection__.restoure_object()
        if self.__expectation__:
            print  self._call_waiting_msg()
    
    def _call_waiting_msg(self):
        return("Call waiting:\n"
               "Expected:\n"
               "%s\n"
               "Got only:\n"
               "%s") % (
                    self.__traceroute_expected__.stackCode(),
                    self.__traceroute__.stackCode())

class MockedCall(object):
    def __init__(self, attribute, args=[], kargs={}, response = None):
        self.attribute = attribute 
        self.args = args 
        self.kargs = kargs 
        self.response = response 

    def __repr__(self):
        return str((self.attribute, self.args, self.kargs))

    def setResponse(self, response):
        self.response = response

    def call(self, attribute, args=[], kargs={}):
        if(self.attribute == attribute 
        and self.args == args 
        and self.kargs == kargs):
            if isinstance(self.response, Exception):
                raise self.response 
            else:
                return self.response 
        else:
            raise MockCallError('Mock Object received unexpected call.')


class MockExpectationError(AssertionError):
    '''Extends AssertionError for unittest compatibility'''

class MockCallError(AssertionError):
    '''Extends AssertionError for unittest compatibility'''
