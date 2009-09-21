
class _TestDouble(object):

    __kargs__ = {}
    __args__ = []

    def __init__(self,  *args, **kargs):
        self.__args__ = args or []
        self.__kargs__ = kargs or {}

    def __repr__(self):
        return self.__kargs__.get('repr', self.__class__.__name__ + ' Object')

    def __methodCalled__(self, *args, **kargs):
        raise SyntaxError("invalid syntax, Method Not Implemented")

    def __call__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __getattribute__(self, x):
        if x == '__class__':
            return self.__kargs__.get('type', type(self))
        return object.__getattribute__(self, x)


    def __item__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __contains__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __eq__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __ge__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __getitem__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __gt__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __le__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __len__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __lt__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __ne__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __delattr__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __delitem__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __add__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __and__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __delattr__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __div__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __divmod__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __floordiv__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __invert__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __long__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __lshift__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __mod__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __mul__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __neg__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __or__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __pos__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __pow__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __radd__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __rand__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __rdiv__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __rfloordiv__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __rlshift__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __rmod__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __rmul__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __ror__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __rrshift__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __rshift__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __rsub__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __rtruediv__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __rxor__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __setitem__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __sizeof__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __sub__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __truediv__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __xor__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

    def __call__(self, *args, **kargs):
        return self.__methodCalled__(*args, **kargs)

