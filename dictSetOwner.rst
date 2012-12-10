================================================================
Gerar um dicionario de Sets e seus respectivos Owners
================================================================

O uso do dicionario será  para identificar os Owners dos Sets na
geração das Foreigns Keys e ou Índices no script SQL/ANSI

    Para teste
    $ python testar_doc.py dictSetOwner.rst ::

    >>> import itertools as itt
    >>> from time import time
    >>> isSet   = lambda line: line.strip().startswith('SET NAME IS')
    >>> isOwner = lambda line: line.strip().startswith('OWNER IS')
    >>> splitIS = lambda line: line.split(' IS ')[1].strip()
    >>> lines   = open(r"schema.txt").readlines()
    >>>
    >>> ### t0 = time()
    >>> findSet       = filter(isSet, lines)
    >>> findOwner     = filter(isOwner, lines)
    >>> dicSetOwner   = {k:v for k, v in zip(map(splitIS, findSet),map(splitIS, findOwner))}
    >>> ### print 'tempo transcorrido:', time()-t0
    >>>
    >>> ### t0 = time()
    >>> ifindSet      = itt.ifilter(isSet, lines)
    >>> ifindOwner    = itt.ifilter(isOwner, lines)
    >>> idicSetOwner  = {k:v for k, v in itt.izip(itt.imap(splitIS, ifindSet),itt.imap(splitIS, ifindOwner))}
    >>> ### print 'tempo transcorrido:', time()-t0
    >>>
    >>> dicSetOwner  == idicSetOwner
    True
