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
from threading import Timer
import inspect

STOPRECORD = False
RECORDING = True


class Dummy(object):
    """Dummy objects are passed around, but never validated.
    """
    __kargs__ = {}
    __args__ = []
    def __init__(self,  *args, **kargs):
        self.__kargs__ = kargs

    def __repr__(self):
        return self.__kargs__.get('repr', 'Dummy Object')
        
    def __getattribute__(self, x):
        if x in dir(Dummy):
            return object.__getattribute__(self, x)
        else:
            return Dummy()

    def __call__(self, *args, **kargs):
        return Dummy()

    def __iter__(self):
        yield Dummy()

    def __str__(self):
        return  self.__kargs__.get('str', 'Dummy Object')

    def __int__(self):
        return  self.__kargs__.get('int', 1)

    def __float__(self):
        return  self.__kargs__.get('float', 1.0)

    def __nonzero__(self):
        return True

    __item__ = __contains__ = __eq__ = __ge__ = __getitem__ =          \
    __gt__ = __le__ = __len__ = __lt__ = __ne__ =                      \
    __delattr__ = __delitem__ = __add__ = __and__ = __delattr__ =      \
    __div__ = __divmod__ = __floordiv__ = __invert__ =                 \
    __long__ = __lshift__ = __mod__ = __mul__ = __neg__ = __or__ =     \
    __pos__ = __pow__ = __radd__ = __rand__ = __rdiv__ = __rfloordiv__=\
    __rlshift__ = __rmod__ = __rmul__ = __ror__ = __rrshift__ =        \
    __rshift__ = __rsub__ = __rtruediv__ = __rxor__ = __setitem__ =    \
    __sizeof__ = __sub__ = __truediv__ = __xor__ = __call__


class Stub(object):
    """Stubs provides canned answers to calls made during the test,
    usually not responding at all to anything outside what's programmed
    in for the test.
    """
    __properties__ = {}
    __recording__ = RECORDING

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
    __espectativa__ = [] # [ChamadaMockda(attribute, args, kargs),]
    __recording__ = RECORDING

    __kargs__ = {}
    __args__ = []
    def __init__(self,  *args, **kargs):
        self.__args__ = []
        self.__kargs__ = kargs
        

    def __repr__(self):
        return self.__kargs__.get('repr', 'Mock Object')

    def __enter__(self):
        self.__espectativa__ = []
        self.__recording__ = RECORDING
        return self

    def __call__(self, *args, **kargs):
        propriedade = getframeinfo(getframe(0)).function
        # propriedade == __call__ or alias
        return self.__propriedadeChamada(propriedade, args, kargs)

    def __propriedadeChamada(self, propriedade, args=[], kargs={}):
        if self.__recording__:
            self.__criarEspectativa(ChamadaMockda(propriedade, args=args, kargs=kargs, retorno=self))
            return self
        else:
            return self.__espectativaMockada(propriedade, args, kargs)

    def __exit__(self, type, value, traceback):
        self.__recording__ = STOPRECORD

    __item__ = __contains__ = __eq__ = __ge__ = __getitem__ = __xor__ =\
    __gt__ = __le__ = __len__ = __lt__ = __ne__ = __setitem__ =        \
    __delattr__ = __delitem__ = __add__ = __and__ = __delattr__ =      \
    __div__ = __divmod__ = __floordiv__ = __invert__ = __sub__ =       \
    __long__ = __lshift__ = __mod__ = __mul__ = __neg__ = __or__ =     \
    __pos__ = __pow__ = __radd__ = __rand__ = __rdiv__ = __rfloordiv__=\
    __rlshift__ = __rmod__ = __rmul__ = __ror__ = __rrshift__ =        \
    __rshift__ = __rsub__ = __rtruediv__ = __rxor__ =  __sizeof__ =    \
    __truediv__ = __call__
     
    def __setattr__(self, attr, value):
        if attr in dir(Mock):
            object.__setattr__(self, attr, value)
        else:
            self.__propriedadeChamada('__setattr__', args=[attr, value])

    def __criarEspectativa(self, attr):
        self.__espectativa__.append(attr)

    def __rshift__(self, resultado):
            self.__espectativa__[-1].setResultado(resultado)

    def __espectativaMockada(self, attr, args=[], kargs={}):
        if not self.__espectativa__:
            raise AssertionError("Object's mocks are not pre-programmed with expectations")
        chamadaMockada = self.__espectativa__.pop(0)
        return chamadaMockada.chamada(attr, args, kargs)

    def __getattr__(self, x):
        return self.__propriedadeChamada('__getattribute__', [x])

    def validate(self):
        if self.__espectativa__:
            raise AssertionError, "Object's mocks are not pre-programmed with expectations"
    
    def __del__(self):
        if self.__espectativa__:
            print "Object's mocks are not pre-programmed with expectations"

class ChamadaMockda(object):
    def __init__(self, atributo, args=[], kargs={}, retorno=None):
        self.atributo = atributo
        self.args = args
        self.kargs = kargs
        self.retorno = retorno
    
    def __repr__(self):
        return str((self.atributo, self.args, self.kargs))

    def setResultado(self, retorno):
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
        raise AssertionError, "Object's mocks are not pre-programmed with expectations:\n%s\nExpected:\n%s"%(
            self._representacaoChamada(self.atributo, self.args, self.kargs),
            self._representacaoChamada(atributo, args, kargs))

    def _representacaoChamada(self, attribute, args, kargs):
        return "%s(%s, %s)"%(
            attribute, 
            ", ".join(args), #args
            ", ".join(["%s=%s"%(k,v) for k,v in kargs.items()])) #kargss

