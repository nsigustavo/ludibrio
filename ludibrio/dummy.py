#-*- coding:utf-8 -*-

from sys import _getframe as getframe
from _testdouble import _TestDouble

class Dummy(_TestDouble):
    """Dummy:
        Objects that are not used directly by the unit under test. Usually,
        dummies are parameters that are merely passed on.
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
            
    def __getattribute__(self, x):
        if x == '__class__':
            return self.__kargs__.get('type', type(self))
        elif x in dir(Dummy):
            return object.__getattribute__(self, x)
        else:
            return self

