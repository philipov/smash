#-- smash.sys.handle

"""

"""


import logging
log     = logging.getLogger( name=__name__ )
# debug   = lambda *a, **b : log.debug( "".join( str( arg ) for arg in a ) )
# info    = lambda *a, **b : log.info(  "".join( str( arg ) for arg in a ) )
debug = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
info  = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
# debug = lambda *a, **b : None

################################

from pathlib import Path
from .config import Config

from . import out
from .out import rprint
from pprint import pprint, pformat


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
class FileHandler:
    ''' figure out what to do with a file'''

    def __init__( self, config:Config, filename:str, refname:str ) :
        self.config = config
        self.filename = filename
        self.refname = refname


#----------------------------------------------------------------------#

@export
class YAMLHandler( FileHandler ) :
    pass

@export
class EXEHandler( FileHandler ) :
    pass

@export
class ScriptHandler( FileHandler ) :
    pass


#----------------------------------------------------------------------#

base_handlers = {
    'yml'    : YAMLHandler,
    'yaml'   : YAMLHandler,
    'exe'    : EXEHandler,
    'sh'     : ScriptHandler
}

#----------------------------------------------------------------------#
