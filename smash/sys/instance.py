#-- smash.sys.instance

"""

"""

import logging

log = logging.getLogger( name=__name__ )
debug = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
info = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )

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

# this is where I can begin to flesh out the idea of config files being actual classes.

@export
class InstanceTemplate :
    '''template specifying an instance structure'''

    def __init__( self, config: Config, filename: str, refname: str ) :
        self.config = config
        self.filename = filename
        self.refname = refname

#----------------------------------------------------------------------#

@export
class SmashTemplate( InstanceTemplate ) :
    ''''a default template for smash instance'''
    pass

#----------------------------------------------------------------------#

base_handlers = {
    'smash' : SmashTemplate,
}

#----------------------------------------------------------------------#
