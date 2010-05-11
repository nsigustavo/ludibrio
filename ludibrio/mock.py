#-*- coding:utf-8 -*-

#TODO: mockar imports respeitando o escopo com frame, pode-se subistituir o importe e validar a achamada
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
    __expectation__ =[]#[ChamadaMockda(attribute, args, kargs),]
    __recording__ = RECORDING 
    __lastPropertyCalled__ = None 


    def __enter__(self):
        self.__expectation__ =[]
        self.__recording__ = RECORDING 
        return self 

    def __methodCalled__(self, *args, **kargs):
        property = self.__lastPropertyCalled__ or getframeinfo(getframe(1))[2]# nome da funcao chamada
        self.__lastPropertyCalled__ = None 
        # property ==  __call__ or alias
        return self.__propertyCalled(property, args, kargs)

    def __propertyCalled(self, property, args=[], kargs={}):
        if self.__recording__:
            self.__newExpectation(ChamadaMockda(property, args = args, kargs = kargs, retorno = self))
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

    def __rshift__(self, retorno):
            self.__expectation__[-1].setretorno(retorno)
    __lshift__ = __rshift__ 

    def __espectativaMockada(self, attr, args=[], kargs={}):
        if not self.__expectation__:
            raise AssertionError("Object's mocks are not pre-programmed with expectations")
        chamadaMockada = self.__expectation__.pop(0)
        return chamadaMockada.chamada(attr, args, kargs)

    def __getattr__(self, x):
        self.__lastPropertyCalled__ = x 
        return self.__propertyCalled('__getattribute__',[x])

    def validate(self):
        if self.__expectation__:
            raise AssertionError, "Object's mocks are not pre-programmed with expectations"

    def __del__(self):
        if self.__expectation__:
            print "Object's mocks are not pre-programmed with expectations"


class ChamadaMockda(object):
    def __init__(self, atributo, args=[], kargs={}, retorno = None):
        self.atributo = atributo 
        self.args = args 
        self.kargs = kargs 
        self.retorno = retorno 

    def __repr__(self):
        return str((self.atributo, self.args, self.kargs))

    def setretorno(self, retorno):
        self.retorno = retorno 

    def chamada(self, atributo, args=[], kargs={}):
        if(self.atributo == atributo 
        and self.args == args 
        and self.kargs == kargs):
            if isinstance(self.retorno, Exception):
                raise self.retorno 
            else:
                return self.retorno 
        else:
            self._erro(atributo, args, kargs)

    def _erro(self, atributo, args, kargs):
        raise AssertionError, "Object's mocks are not pre-programmed with expectations.\nGot:\n%s\nExpected:\n%s"%(
            self._representacaoChamada(atributo, args, kargs),
            self._representacaoChamada(self.atributo, self.args, self.kargs)
            )

    def _representacaoChamada(self, attribute, args, kargs):
        if attribute == '__getattribute__':
            return args[0]
        return "%s(%s)"%(
                attribute, 
                ", ".join(["%r"%arg for arg in args]+["%s=%r"%(k, v)for k, v in kargs.items()]))

