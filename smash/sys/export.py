#-- smash.sys.export

"""
write output files from compiled configtree node
"""


import logging
log     = logging.getLogger( name='smash.sys.export' )
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
class Exporter:
    ''' methods for writing contents of configtree to an output file'''

    def __init__( self, config:Config, filename:str, refname:str ) :
        self.config = config
        self.filename = filename
        self.refname = refname


    def write( self, target_path: Path ) :
        raise NotImplementedError

    def export( self ) :
        self.write( self.config.path )


#----------------------------------------------------------------------#

@export
class ExportEnvironment( Exporter ):
    pass


#----------------------------------------------------------------------#

@export
class ExportDebug( Exporter ) :
    pass

#----------------------------------------------------------------------#

base_exporters = {
    'Exporter':             Exporter,
    'ExportEnvironment':    ExportEnvironment,
    'ExportDebug':          ExportDebug
}

#----------------------------------------------------------------------#
