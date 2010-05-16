#-*- coding:utf-8 -*-

from sys import _getframe as getframe
from _testdouble import _TestDouble

class Dummy(_TestDouble):
    """Dummy:
        São objetos que não são utilizados diretamente pela unidade sob teste.
        Normalmente paramentros que somente são repassados
    """
    def __methodCalled__(self, *args, **kargs):
        return self

    def __iter__(self):
        yield self

    def __str__(self):
        return self.__kargs__.get('str', 'Dummy Object')

    def __int__(self):
        return self.__kargs__.get('int', 1)

    def __float__(self):
        return self.__kargs__.get('float', 1.0)

    def __nonzero__(self):
        return True

    def __getattr__(self, x):
        if x in dir(Dummy):
            return object.__getattribute__(self, x)
        else:
            return self


