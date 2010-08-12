from ludibrio import Stub

class Spy(Stub):

    __calls__ = [] #[attr, args=[], kargs={}]

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
        return times.verify(
                self.spy.called_count([self._attr_called,
                                       self.args,
                                       self.kargs]))
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
        return self._handle(lambda x, y: x == y,
                             expectation_value)        

    def __gt__(self, expectation_value):
        return self._handle(lambda x, y: x > y,
                             expectation_value)       
        
    def __ge__(self, expectation_value):
        return self._handle(lambda x, y: x >= y,
                             expectation_value)
    
    def __lt__(self, expectation_value):
        return self._handle(lambda x, y: x < y,
                             expectation_value)
        
    def __le__(self, expectation_value):
        return self._handle(lambda x, y: x <= y,
                             expectation_value)

    def verify(self, value):
        return self.operation(value, self.expectation_value)

times = Times()

class Before(object):
    def __init__(self, verify_object):
        self.verify_object = verify_object
    
    def __getattr__(self, attr):
        self.attr_called = [attr]
        return self

    def __call__(self, *args, **kargs):
        self.attr_called += [args, kargs]
        
        attr = self.verify_object._attr_called
        args = self.verify_object.args
        kargs = self.verify_object.kargs
        
        before = [attr, args, kargs]
        after = self.attr_called    
        calls = self.verify_object.spy.__calls__
        try:
            return calls.index(before) < calls.index(after)
        except ValueError:
            return False            

class After(object):
    def __init__(self, verify_object):
        self.verify_object = verify_object
    
    def __getattr__(self, attr):
        self.attr_called = [attr]
        return self

    def __call__(self, *args, **kargs):
        self.attr_called += [args, kargs]
        
        attr = self.verify_object._attr_called
        args = self.verify_object.args
        kargs = self.verify_object.kargs
        
        before = [attr, args, kargs]
        after = self.attr_called    
        calls = self.verify_object.spy.__calls__
        try:
            return calls.index(before) > calls.index(after)
        except ValueError:
            return False            


#class After(TimeCalled):
#    def compare(self):
#        try:..except

#class Before(TimeCalled):
#    def compare(self):
#        try..except

#class TimeCalled(object):
#    ...
#    def __call__(...)
#        return self.compare(...)
