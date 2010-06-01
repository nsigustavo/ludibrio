from ludibrio.specialarguments import matcher
import re

class ParameterException(Exception):
    """'Exception' for mandatory parameters"""

@matcher
def any(x, y):
    return True

@matcher
def equal_to(x, y):
    if  x == y: return True
    raise ParameterException("%r is not equal to %r"%(x, y))

@matcher
def into(item, container):
    if item in container: return True
    raise ParameterException("%r is not in %r"%(item, container))

@matcher
def contains(container, item):
    if item in container: return True
    raise ParameterException("%r is not contains %r"%(container, item))

@matcher
def greater_than(x, y):
    if x > y: return True
    raise ParameterException("%r is not greater than %r"%(x, y))

@matcher
def greater_than_or_equal_to(x, y):
    if x >= y: return True
    raise ParameterException("%r is not greater than or equal to %r"%(x, y))

@matcher
def less_than(x, y):
    if x < y: return True
    raise ParameterException("%r is not less than %r"%(x, y))

@matcher
def less_than_or_equal_to(x, y):
    if x <= y: return True
    raise ParameterException("%r is not less than or equal to %r"%(x, y))

@matcher
def in_any_order(container, elements):
    for element in elements:
        if element not in container:
            raise ParameterException("%r does not have in any order %r"%(container, elements))
    return True

@matcher
def any_of(container, elements):
    for element in elements:
        if element in container:
            return True
    raise ParameterException("%r does not have any of %r"%(container, elements))

@matcher
def kind_of(obj, kind):
    if isinstance(obj, kind): return True
    raise ParameterException("%r is not a kind of %r"%(obj, kind))

@matcher
def instance_of(obj, kind):
    if isinstance(obj, kind): return True
    raise ParameterException("%r is not a instance of %r"%(obj, kind))

@matcher
def ended_with(x, y):
    if x.endswith(y): return True
    raise ParameterException("%r is not ended with %r"%(x, y))

@matcher
def started_with(x, y):
    if x.startswith(y): return True
    raise ParameterException("%r is not started with %r"%(x, y))


@matcher
def like(string, regex):
    if re.match(regex, string) is not None:
        return True
    raise ParameterException("%r is not like %r"%(string, regex))


@matcher
def equal_to_ignoring_case(x, y):
    if unicode(x, 'utf-8').lower() == unicode(y, 'utf-8').lower():
        return True
    raise ParameterException("%r is not equal to %r ignoring case"%(x, y))


