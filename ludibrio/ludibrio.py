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

#TODO: mockar importes respeitando o escopo com frame, pode-se subistituir o importe e validar a achamada
#TODO: Spy ainda esta como protótipo

from __future__ import with_statement
from inspect import getframeinfo
from sys import _getframe as getframe
from types import MethodType, UnboundMethodType, FunctionType
from _testdouble import _TestDouble
funcsType = [ MethodType, UnboundMethodType, FunctionType]
STOPRECORD = False
RECORDING = True

class notCalleble(object):
    def __call__(self, func):
        def newmethod(dummy, *args, **kargs):
            ob = dummy.__kargs__.get('must_not_be_used_by', None)
            if ob:
                if isinstance(ob, object):
                    contexts = [getattr(ob, f).im_func.func_code for f in dir(ob) if type(getattr(ob, f)) in funcsType ]
                else:
                    contexts = [ob.im_func.func_code]
                frame = getframe(1)
                if frame.f_code in contexts:
                    raise AttributeError, "Dummy Object must not be called"
            return func(dummy, *args, **kargs)
        return newmethod
    def f(self):pass



class Dummy(_TestDouble):
    """Dummy objects are passed around, but never validated.
    """

    @notCalleble()
    def __methodCalled__(self, *args, **kargs):
        return Dummy()

    @notCalleble()
    def __iter__(self):
        yield Dummy()

    @notCalleble()
    def __str__(self):
        return  self.__kargs__.get('str', 'Dummy Object')

    @notCalleble()
    def __int__(self):
        return  self.__kargs__.get('int', 1)

    @notCalleble()
    def __float__(self):
        return  self.__kargs__.get('float', 1.0)

    def __nonzero__(self):
        return True

    @notCalleble()
    def __getattr__(self, x):
        if x in dir(Dummy):
            return object.__getattribute__(self, x)
        else:
            return Dummy()


class Stub(_TestDouble):
    """Stubs provides canned answers to calls made during the test.
    """
    __expectation__= [] # [(attribute, args, kargs),]
    __recording__ = RECORDING
    __lastPropertyCalled__ = None
    __import__ = None


    def __restaureImport(self):
        self.__import__.restaure()

    def __enter__(self):
        self.__expectation__= []
        self.__recording__ = RECORDING
        self.__import__ = SavedImport(self)
        return self

    def __methodCalled__(self, *args, **kargs):
        property =  self.__lastPropertyCalled__ or getframeinfo(getframe(1))[2]#nome da funcao chamada
        # property == __call__ or alias
        self.__lastPropertyCalled__ = None
        return self.__propertyCalled(property, args, kargs)

    def __propertyCalled(self, property, args=[], kargs={}, retorno=None):
        if self.__recording__:
            self.__newExpectation([property, args, kargs, retorno])
            return self
        else:
            return self.__expectationValue(property, args, kargs)

    def __exit__(self, type, value, traceback):
        self.__recording__ = STOPRECORD
        self.__restaureImport()

    def __setattr__(self, attr, value):
        if attr in dir(Stub):
            object.__setattr__(self, attr, value)
        else:
            self.__propertyCalled('__setattr__', args=[attr, value])

    def __newExpectation(self, attr):
        self.__expectation__.append(attr)

    def __rshift__(self, retorno):
            self.__expectation__[-1][3] = retorno
    __lshift__ = __rshift__

    def __expectationValue(self, attr, args=[], kargs={}):
        for position, (attrEsp, argsEsp, kargsEsp, retorno) in enumerate(self.__expectation__):
            if (attrEsp, argsEsp, kargsEsp) == (attr, args, kargs):
                self.__toTheEnd__(position)
                return retorno

        return Dummy()

    def __toTheEnd__(self, position):
        self.__expectation__.append(self.__expectation__.pop(position))

    def __getattr__(self, x):
        self.__lastPropertyCalled__ = x
        return self.__propertyCalled('__getattribute__', (x,), retorno=self)

    def __del__(self):
        self._import.restoreObjet()





class Spy(Stub):
    def __init__(self, type , *args, **kargs):
        kargs['type']=type
        Stub(self, *args, **kargs)

    def __expectationValue(self, attr, args=[], kargs={}):
        for position, (attrEsp, argsEsp, kargsEsp, retorno) in enumerate(self.__expectation__):
            if (attrEsp, argsEsp, kargsEsp) == (attr, args, kargs):
                self.__toTheEnd(position)
                return retorno
        return getattr(self.__kargs__.get('type'), attr)(*args, **kargs)


class SavedImport(object):

    def __init__(self, testeDouble):
        self.testeDouble = testeDouble
        self._import = __import__ = __builtins__['__import__']
        __import__ = __builtins__['__import__'] = self

    def __call__(self, name, globals={}, locals={}, fromlist=[], level=-1):
        self.objetOriginal = self._import(name, globals, locals, fromlist, level)
        if fromlist is not None:
            self.modulo = self._import(name, globals, locals, None, level)
            self.objectName = fromlist[0]
            setattr(self.modulo, self.objectName, self.testeDouble)
        return self._import(name, globals, locals, fromlist, level)

    def restaure(self):
        __builtins__['__import__'] = __import__ = self._import

    def restoreObjet(self):
        setattr(self.modulo, self.objectName, self.objetOriginal)

class Mock(_TestDouble):
    """Mocks are what we are talking about here:
    objects pre-programmed with expectations which form a
    specification of the calls they are expected to receive.
    """
    __expectation__= [] # [ChamadaMockda(attribute, args, kargs),]
    __recording__ = RECORDING
    __import__ = None
    __lastPropertyCalled__ = None

    def __restaureImport(self):
        self.__import__.restaure()

    def __enter__(self):
        self.__expectation__= []
        self.__recording__ = RECORDING
        self.__import__ = SavedImport(self)
        return self

    def __methodCalled__(self, *args, **kargs):
        property = self.__lastPropertyCalled__ or getframeinfo(getframe(1))[2]# nome da funcao chamada
        self.__lastPropertyCalled__= None
        # property == __call__ or alias
        return self.__propertyCalled(property, args, kargs)

    def __propertyCalled(self, property, args=[], kargs={}):
        if self.__recording__:
            self.__newExpectation(ChamadaMockda(property, args=args, kargs=kargs, retorno=self))
            return self
        else:
            return self.__espectativaMockada(property, args, kargs)

    def __exit__(self, type, value, traceback):
        self.__recording__ = STOPRECORD
        self.__restaureImport()

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
        return self.__propertyCalled('__getattribute__', [x])

    def validate(self):
        if self.__expectation__:
            raise AssertionError, "Object's mocks are not pre-programmed with expectations"

    def __del__(self):
        self._import.restoreObjet()
        if self.__expectation__:
            print "Object's mocks are not pre-programmed with expectations"


class ChamadaMockda(object):
    def __init__(self, atributo, args=[], kargs={}, retorno=None):
        self.atributo = atributo
        self.args = args
        self.kargs = kargs
        self.retorno = retorno

    def __repr__(self):
        return str((self.atributo, self.args, self.kargs))

    def setretorno(self, retorno):
        self.retorno = retorno

    def chamada(self, atributo, args=[], kargs={}):
        if( self.atributo == atributo
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
            ", ".join(["%r"%arg for arg in args] + ["%s=%r"%(k,v) for k,v in kargs.items()]))

