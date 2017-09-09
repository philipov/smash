#-- smash.sys.export

"""
write output files from compiled configtree node
"""


import logging
log     = logging.getLogger( name=__name__ )
debug = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
info  = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )

################################

import sys

from collections import OrderedDict
from collections import namedtuple
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

    def __init__( self, config:Config, sections, destination ) :
        self.config         = config
        self.sections       = sections
        self.destination    = destination


    def write( self, config:Config, sections:list, destination:str ):
        raise NotImplementedError


    @property
    def result( self, ) :
        return self.write(self.config, self.sections, self.destination)


################################




#----------------------------------------------------------------------#

@export
class ExportShell( Exporter ):

    class AmbiguousKeyError( Exception ) :
        '''two sections exported to the same destination have matching keys'''

        def __init__( self, *args, **kwargs ) :
            super( ).__init__(
                namedtuple( '_', ['conflicting_sections', 'key', 'values', 'config', 'destination'] )( *args ), **kwargs )
    #####

    pathlist_delimiter = ';' if sys.platform=='win32' else ':'

    def pathlist2string(self, paths:list) -> str:
        pathlist = list()
        for value in paths:
            if isinstance(value, str):
                pathlist.append(value)
                continue
            if isinstance(value, list):
                pathlist.extend(value)
                continue
            raise TypeError("Can't append to pathlist: "+str(value)+" | "+str(type(value)))

        return self.pathlist_delimiter.join(pathlist)

    def write( self, config: Config, sections:list, destination:None ) -> OrderedDict:
        subenv      = OrderedDict()
        keysources  = OrderedDict()
        for section in sections:
            for key, value in config[section].allitems():
                if key not in subenv:
                    if isinstance(value, str):
                        subenv[key]     = str(value)
                        keysources[key] = section
                    elif isinstance(value, list):
                        subenv[key]     = self.pathlist2string( value )
                        keysources[key] = section
                    else:
                        raise TypeError('Invalid environment value',
                                    namedtuple('_',['section', 'key', 'value', 'type' ])
                                                    (section, key, str(value), str(type(value))))
                    info( out.red( 'ExportEnvironment' ), " {:<20} = {:64}".format(str(key), subenv[key])  )
                else:
                    raise self.AmbiguousKeyError((section, keysources[key]), key, (value, subenv[key]) ,str(config), destination)

        return subenv


#----------------------------------------------------------------------#

@export
class ExportDebug( Exporter ) :
    def write( self, config: Config, sections, destination ) -> None:
        raise NotImplementedError


#----------------------------------------------------------------------#

@export
class ExportYAML( Exporter ) :
    def write( self, config: Config, sections, destination ) -> None:
        raise NotImplementedError


#----------------------------------------------------------------------#

@export
class ExportXML( Exporter ) :
    def write( self, config: Config, sections, destination ) -> None:
        raise NotImplementedError


#----------------------------------------------------------------------#

@export
class ExportINI( Exporter ) :
    pathlist_delimiter = ','

    def pathlist2string( self, paths: list ) -> str :
        pathlist = list( )
        for value in paths :
            if isinstance( value, str ) :
                pathlist.append( value )
                continue
            raise TypeError( "Can't append to pathlist: " + str( value ) + " | " + str( type( value ) ) )

        return self.pathlist_delimiter.join( pathlist )

    def write( self, config: Config, sections: list, destination: None ) -> OrderedDict :
        subenv = OrderedDict( )
        keysources = OrderedDict( )
        for section in sections :
            for key, value in config[section].allitems( ) :
                if key not in subenv :
                    if isinstance( value, str ) :
                        subenv[key] = str( value )
                        keysources[key] = section
                    elif isinstance( value, list ) :
                        subenv[key] = self.pathlist2string( value )
                        keysources[key] = section
                    else :
                        raise TypeError( 'Invalid environment value',
                                         namedtuple( '_', ['section', 'key', 'value', 'type'] )
                                         ( section, key, str( value ), str( type( value ) ) ) )
                    info( out.red( 'ExportEnvironment' ), " {:<20} = {:64}".format( str( key ), subenv[key] ) )
                else :
                    raise self.AmbiguousKeyError( (section, keysources[key]), key, (value, subenv[key]), str( config ),
                                                  destination )

#----------------------------------------------------------------------#

base_exporters = {
    'Shell' : ExportShell,
    'Debug' : ExportDebug,
    'YAML'  : ExportYAML,
    'XML'   : ExportXML,
    'INI'   : ExportINI
}

#----------------------------------------------------------------------#
