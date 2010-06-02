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
--------

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

