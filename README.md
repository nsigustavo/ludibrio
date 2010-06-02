Ludibrio
========

Author
------

Gustavo Rezende <nsigustavo@gmail.com>



Development
-----------

Development of Ludibrio may be tracked in github:
http://github.com/nsigustavo/ludibrio

The source code may be obtained using 'git':
    git clone git://github.com/nsigustavo/ludibrio.git

Code may be browsed at:
    http://github.com/nsigustavo/ludibrio


Tutorial
========


Install
-------

    $ sudo easy_install ludibrio


Mock
----

Mocks are what we are talking about here: objects pre-programmed with expectations which form a specification of the calls they are expected to receive.

A Mocker or Stub instance is used to command with recording and replaying of expectations.

    >>> from ludibrio import Mock
    
    >>> with Mock() as MySQLdb:
    ...     con = MySQLdb.connect('servidor', ' usuario', 'senha')
    ...     con.select_db('banco de dados') >> None
    ...     cursor = con.cursor()
    ...     cursor.execute('ALGUM SQL') >> None
    ...     cursor.fetchall() >> [1,2,3,4,5]
    >>> con = MySQLdb.connect('servidor', ' usuario', 'senha')
    >>> con.select_db('banco de dados')
    >>> cursor = con.cursor()
    >>> cursor.execute('ALGUM SQL')
    >>> cursor.fetchall()
    [1, 2, 3, 4, 5]
    
    >>> MySQLdb.validate() #passed


Stub
----

Stubs provide canned answers to calls made during the test.

    >>> from ludibrio import Stub

    >>> with Stub() as x:
    ...     x.anything() >> 'responce'

    >>> x.anything()
    'responce'


Trivial mocking or stubing of any external module
-------------------------------------------------

Ludibrio also offers a replace mode, which basically means that if using the "from ... import ..." in 'with', on replay time the returned mock object will replace the original object in namespaces of the whole Python interpreter (including modules, etc). Here is a simple example to illustrate how it may be used:

    >>> from ludibrio import Stub
    
    >>> with Stub() as time:
    ...     from time import time
    ...     time() >> 171

    >>> from time import time
    >>> time()
    171



Proxy
-----
Two powerful features of Ludibrio which aren't commonly seen in other mocking systems is the ability of proxying to existing objects, or even patching the real instance or class.

When an object is proxied, Ludibrio will create a Test Double object which will hold a reference to the real object, and will allow expressions to passthrough (mocked or not, and by default or on request).

    >>> from os.path import splitext

    >>> with Stub(proxy=splitext) as splitext:
    ...     splitext('ludibrio/stubed.py') >> ('/temp/temp','.temp')
    
    >>> splitext('mock.py')
    ('mock', '.py')
    
    >>> splitext('ludibrio/stubed.py')
    ('/temp/temp', '.temp')
    
    
