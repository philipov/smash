#-- smash.sys.export

"""
write output files from compiled configtree node
"""


import logging
log     = logging.getLogger( name=__name__ )
debug = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
info  = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )

################################

from collections import OrderedDict
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
class Exporter:
    ''' methods for writing contents of configtree to an output file'''

    @classproperty
    def __key__(cls):
        return cls.__name__

    def __init__( self, config:Config ) :
        self.config = config


    def write( self, target_path: Path ):
        raise NotImplementedError

    def export( self ) :
        self.write( self.config.path )


#----------------------------------------------------------------------#

@export
class ExportEnvironment( Exporter ):
    def write( self, target_path: Path ) -> OrderedDict:
        result = OrderedDict()

        return result


#----------------------------------------------------------------------#

@export
class ExportDebug( Exporter ) :
    def write( self, target_path: Path ) -> None:
        raise NotImplementedError


#----------------------------------------------------------------------#

@export
class ExportYAML( Exporter ) :
    def write( self, target_path: Path ) -> None:
        raise NotImplementedError


#----------------------------------------------------------------------#

@export
class ExportXML( Exporter ) :
    def write( self, target_path: Path ) -> None:
        raise NotImplementedError


#----------------------------------------------------------------------#

@export
class ExportINI( Exporter ) :
    def write( self, target_path: Path ) -> None:
        for key in self.config.keys():
            pass

#----------------------------------------------------------------------#

base_exporters = {
    'Environment' : ExportEnvironment,
    'Debug'       : ExportDebug,
    'YAML'        : ExportYAML,
    'XML'         : ExportXML,
    'INI'         : ExportINI
}

#----------------------------------------------------------------------#
