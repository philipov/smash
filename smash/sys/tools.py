#-- smash.sys.tools

"""
wrappers for subprocesses
"""


import logging
log     = logging.getLogger( name=__name__ )
debug = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
info  = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )

################################

from pathlib import Path
from .config import Config

from ..utils import out
from ..utils.out import rprint
from pprint import pprint, pformat

from ..utils.meta import classproperty
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
class Tool:
    ''' figure out what to do with a file'''

    def __init__( self, config:Config, filename:str, refname:str ) :
        self.config = config
        self.filename = filename
        self.refname = refname


#----------------------------------------------------------------------#

@export
class Task( Tool ) :
    '''perform an action once'''
    pass

@export
class Loader( Task ) :
    pass

@export
class Validator( Task ) :
    pass


################################
@export
class Daemon( Tool ) :
    '''keep repeating an action until killed'''
    pass

@export
class Monitor( Daemon ) :
    pass

@export
class Service( Daemon ) :
    pass

#----------------------------------------------------------------------#

base_tools = {
    'Task'      : Task,
    'Loader'    : Loader,
    'Validator' : Validator,
    'Monitor'   : Monitor,
    'Service'   : Service,
}



#----------------------------------------------------------------------#
