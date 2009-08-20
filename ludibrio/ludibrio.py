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
from types import MethodType, UnboundMethodType, FunctionType

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


class Dummy(object):
    """Dummy objects are passed around, but never validated.
    """
    __kargs__ = {}
    __args__ = []

    def __init__(self,  *args, **kargs):
        self.__kargs__ = kargs

    def __repr__(self):
        return self.__kargs__.get('repr', 'Dummy Object')

    @notCalleble()
    def __call__(self, *args, **kargs):
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

    __item__ = __contains__ = __eq__ = __ge__ = __getitem__ =          \
    __gt__ = __le__ = __len__ = __lt__ = __ne__ =                      \
    __delattr__ = __delitem__ = __add__ = __and__ = __delattr__ =      \
    __div__ = __divmod__ = __floordiv__ = __invert__ =                 \
    __long__ = __lshift__ = __mod__ = __mul__ = __neg__ = __or__ =     \
    __pos__ = __pow__ = __radd__ = __rand__ = __rdiv__ = __rfloordiv__=\
    __rlshift__ = __rmod__ = __rmul__ = __ror__ = __rrshift__ =        \
    __rshift__ = __rsub__ = __rtruediv__ = __rxor__ = __setitem__ =    \
    __sizeof__ = __sub__ = __truediv__ = __xor__ = __call__

    @notCalleble()
    def __getattr__(self, x):
        if x in dir(Dummy):
            return object.__getattribute__(self, x)
        else:
            return Dummy()

class Stub(object):
    """Stubs provides canned answers to calls made during the test.
    """
    __espectativa__ = [] # [(attribute, args, kargs),]
    __recording__ = RECORDING
    __kargs__ = {}
    __args__ = []

    __ultimapropriedadechamada__ = None
    
    def __init__(self,  *args, **kargs):
        self.__args__ = []
        self.__kargs__ = kargs

    def __repr__(self):
        return self.__kargs__.get('repr', 'Stub Object')

    def __enter__(self):
        self.__espectativa__ = []
        self.__recording__ = RECORDING
        return self

    def __call__(self, *args, **kargs):
        propriedade = self.__ultimapropriedadechamada__ or getframeinfo(getframe(0)).function
        # propriedade == __call__ or alias
        self.__ultimapropriedadechamada__ = None
        return self.__propriedadeChamada(propriedade, args, kargs)

    def __propriedadeChamada(self, propriedade, args=[], kargs={}, retorno=None):
        if self.__recording__:
            self.__criarEspectativa([propriedade, args, kargs, retorno])
            return self
        else:
            return self.__valorEsperado(propriedade, args, kargs)

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
        if attr in dir(Stub):
            object.__setattr__(self, attr, value)
        else:
            self.__propriedadeChamada('__setattr__', args=[attr, value])

    def __criarEspectativa(self, attr):
        self.__espectativa__.append(attr)

    def __rshift__(self, retorno):
            self.__espectativa__[-1][3] = retorno
    __lshift__ = __rshift__

    def __valorEsperado(self, attr, args=[], kargs={}):
        for position, (attrEsp, argsEsp, kargsEsp, retorno) in enumerate(self.__espectativa__):
            if (attrEsp, argsEsp, kargsEsp) == (attr, args, kargs):
                self.__vaParaOFinal(position)
                return retorno
        return Dummy()

    def __vaParaOFinal(self, position):
        self.__espectativa__.append(self.__espectativa__.pop(position))
    

    def __getattr__(self, x):
        self.__ultimapropriedadechamada__ = x
        return self.__propriedadeChamada('__getattribute__', (x,), retorno=self)


class SavedImport(object):

    def __init__(self, mock):
        self.mock = mock
        self._import = __import__ = __builtins__['__import__']
        __import__ = __builtins__['__import__'] = self

    def __call__(self, name, globals={}, locals={}, fromlist=[], level=-1):
        if fromlist is not None:
            modulo = self._import(name, globals, locals, None, level)
            setattr(modulo, fromlist[0], self.mock)
        return self._import(name, globals, locals, fromlist, level)
    def restaure(self):
        __builtins__['__import__'] = __import__ = self._import

class Mock(object):
    """Mocks are what we are talking about here:
    objects pre-programmed with expectations which form a
    specification of the calls they are expected to receive.
    """
    __espectativa__ = [] # [ChamadaMockda(attribute, args, kargs),]
    __recording__ = RECORDING
    __import = None
    __kargs__ = {}
    __args__ = []
        
    def __init__(self,  *args, **kargs):
        self.__args__ = []
        self.__kargs__ = kargs

    def __repr__(self):
        return self.__kargs__.get('repr', 'Mock Object')

    def __restaureImport(self):
        self.__import.restaure()


    def __enter__(self):
        self.__espectativa__ = []
        self.__recording__ = RECORDING
        self.__import = SavedImport(self)
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
        self.__restaureImport()

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

    def __rshift__(self, retorno):
            self.__espectativa__[-1].setretorno(retorno)
    __lshift__ = __rshift__

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
        raise AssertionError, "Object's mocks are not pre-programmed with expectations:\n%s\nExpected:\n%s"%(
            self._representacaoChamada(self.atributo, self.args, self.kargs),
            self._representacaoChamada(atributo, args, kargs))

    def _representacaoChamada(self, attribute, args, kargs):
        return "%s(%s, %s)"%(
            attribute, 
            ", ".join(args), #args
            ", ".join(["%s=%s"%(k,v) for k,v in kargs.items()])) #kargss

