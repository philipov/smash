#-- smash.core.handler

"""

"""


import logging
log     = logging.getLogger( name=__name__ )
debug = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
info  = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )

################################

from pathlib import Path
from .config import Config

from ..util import out
from ..util.out import rprint
from pprint import pprint, pformat

from ..util.meta import classproperty

from collections import OrderedDict

#----------------------------------------------------------------------#

__all__ = []

def export( obj ) :
    try :
        __all__.append( obj.__name__ )
    except AttributeError :
        __all__.append( obj.__main__.__name__ )
    return obj



#----------------------------------------------------------------------#

@export
class Handler:
    ''' figure out what to do with a file'''

    def __init__( self, config:Config, filename:str, refname:str ) :
        self.config = config
        self.filename = filename
        self.refname = refname

#----------------------------------------------------------------------#
@export
class FileHandler(Handler):
    pass


#----------------------------------------------------------------------#

@export
class YAMLHandler( FileHandler ) :
    pass


#----------------------------------------------------------------------#
@export
class EXEHandler( FileHandler ) :
    pass


#----------------------------------------------------------------------#
@export
class ScriptHandler( FileHandler ) :
    pass


#----------------------------------------------------------------------#
@export
class BashHandler( ScriptHandler ) :
    pass


#----------------------------------------------------------------------#
@export
class BatchHandler( ScriptHandler ) :
    pass


#----------------------------------------------------------------------#

### last in first out; use the first handler whose key regex matches the filename
builtin_handlers            = OrderedDict()
builtin_handlers['.*']      = FileHandler

builtin_handlers['\.yml']   = YAMLHandler
builtin_handlers['\.yaml']  = YAMLHandler

builtin_handlers['\.exe']   = EXEHandler
builtin_handlers['\.sh']    = BashHandler
builtin_handlers['\.bat']   = BatchHandler


#----------------------------------------------------------------------#
