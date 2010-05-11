#-*- coding:utf-8 -*-

#TODO: mockar imports respeitando o escopo com frame, pode-se subistituir o importe e validar a acall
#TODO: Spy ainda esta como protótipo

from __future__ import with_statement 
from inspect import getframeinfo 
from sys import _getframe as getframe 
from types import MethodType, UnboundMethodType, FunctionType 
from _testdouble import _TestDouble 


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
    __lastPropertyCalled__ = None 


    def __enter__(self):
        self.__expectation__ =[]
        self.__recording__ = RECORDING 
        return self 

    def __methodCalled__(self, *args, **kargs):
        property = self.__lastPropertyCalled__ or getframeinfo(getframe(1))[2]# nome da funcao call
        self.__lastPropertyCalled__ = None 
        # property ==  __call__ or alias
        return self.__propertyCalled(property, args, kargs)

    def __propertyCalled(self, property, args=[], kargs={}):
        if self.__recording__:
            self.__newExpectation(MockedCall(property, args = args, kargs = kargs, response = self))
            return self 
        else:
            return self.__espectativaMockada(property, args, kargs)

    def __exit__(self, type, value, traceback):
        self.__recording__ = STOPRECORD 

    def __setattr__(self, attr, value):
        if attr in dir(Mock):
            object.__setattr__(self, attr, value)
        else:
            self.__propertyCalled('__setattr__', args=[attr, value])

    def __newExpectation(self, attr):
        self.__expectation__.append(attr)

    def __rshift__(self, response):
            self.__expectation__[-1].setResponse(response)
    __lshift__ = __rshift__ 

    def __espectativaMockada(self, attr, args=[], kargs={}):
        if not self.__expectation__:
            raise MockExpectationError("Mock Object received unexpected call: %s" % self.__lastPropertyCalled__)
        callMockada = self.__expectation__.pop(0)
        return callMockada.call(attr, args, kargs)

    def __getattr__(self, x):
        self.__lastPropertyCalled__ = x 
        return self.__propertyCalled('__getattribute__',[x])

    def validate(self):
        if self.__expectation__:
            raise MockExpectationError("Mock Object expected %s(), but didn't "
                                 "received it" % self.__expectation__[0].args[0])

    def __del__(self):
        if self.__expectation__:
            print "Object's mocks are not pre-programmed with expectations"


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
            self._erro(attribute, args, kargs)

    def _erro(self, attribute, args, kargs):
        raise MockExpectationError, "Mock Object received unexpected call.\nExpected:\n%s\nGot:\n%s"%(
            self._callRepresentation(self.attribute, self.args, self.kargs),
            self._callRepresentation(attribute, args, kargs),
            )

    def _callRepresentation(self, attribute, args, kargs):
        if attribute == '__getattribute__':
            return args[0]
        return "%s(%s)"%(
                attribute, 
                ", ".join(["%r"%arg for arg in args]+["%s=%r"%(k, v)for k, v in kargs.items()]))


class MockExpectationError(AssertionError):
    '''Extends AssertionError for unittest compatibility'''
