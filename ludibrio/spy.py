from ludibrio import Stub
from ludibrio.helpers import format_called


class Spy(Stub):

    __calls__ = []

    def _expectation_value(self, attr, args=[], kargs={}):
        self.__calls__.append([attr, args, kargs])
        for position, (attr_expectation, args_expectation, kargs_expectation, response) in enumerate(self.__expectation__):
            if (attr_expectation, args_expectation, kargs_expectation) == (attr, args, kargs):
                self._to_the_end(position)
                return response
        if self._has_proxy():
            return self._proxy(attr, args, kargs)
        return self
        
    def __repr__(self):
        return 'Spy Object'
    
        
    def called_count(self, expectation):
        count = 0
        for call in self.__calls__:
            if call == expectation:
                count+=1
        return count


class verify(object):

    def __init__(self, spy):
        self.spy = spy

    def __getattr__(self, attr):
        self._attr_called = attr
        return self

    def __call__(self, *args, **kargs):
        self.args = args
        self.kargs = kargs
        return self  

    def called(self, times):
        called_count = self.spy.called_count([self._attr_called,
                                              self.args,
                                              self.kargs])
        if not times.verify(called_count):
            raise SpyExpectationError("Spy expected %s %s%d times but received %d" % (
                                        format_called(self._attr_called,
                                                      self.args,
                                                      self.kargs), 
                                        times.operator_message,
                                        times.expectation_value, 
                                        called_count))
    
    @property
    def before(self):        
        return Before(self)

    @property
    def after(self):
        return After(self)


class Times(object):
    
    def _handle(self, operation, expectation_value):
        self.operation = operation
        self.expectation_value = expectation_value
        return self

    def __eq__(self, expectation_value):
        self.operator_message = ''
        return self._handle(lambda x, y: x == y,
                             expectation_value)        

    def __gt__(self, expectation_value):
        self.operator_message = 'more than '
        return self._handle(lambda x, y: x > y,
                             expectation_value)       
        
    def __ge__(self, expectation_value):
        self.operator_message = 'more than or equal to '
        return self._handle(lambda x, y: x >= y,
                             expectation_value)
    
    def __lt__(self, expectation_value):
        self.operator_message = 'less than '
        return self._handle(lambda x, y: x < y,
                             expectation_value)
        
    def __le__(self, expectation_value):
        self.operator_message = 'less than or equal to '
        return self._handle(lambda x, y: x <= y,
                             expectation_value)

    def verify(self, value):
        return self.operation(value, self.expectation_value)


times = Times()


class TimeCalled(object):
    
    def __init__(self, verify_object):
        attr = verify_object._attr_called
        args = verify_object.args
        kargs = verify_object.kargs
        self.calls = verify_object.spy.__calls__
        self.before = [attr, args, kargs]
    
    def __getattr__(self, attr):
        self.attr_called = [attr]
        return self

    def __call__(self, *args, **kargs):
        self.attr_called += [args, kargs]
        self.after = self.attr_called
        return self.compare()


class Before(TimeCalled):
    def compare(self):
        if not self.calls.index(self.before) < self.calls.index(self.after):
            raise SpyExpectationError("Spy expected %s called before %s" %
                                           (format_called(*self.before), format_called(*self.after)))

class After(TimeCalled):
    def compare(self):
        if not self.calls.index(self.before) > self.calls.index(self.after):
            raise SpyExpectationError("Spy expected %s called after %s" %
                                           (format_called(*self.before), format_called(*self.after)))


class SpyExpectationError(AssertionError):
    """Extends AssertionError for unittest compatibility"""
