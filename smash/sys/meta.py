#-- smash.sys.meta

"""
utilities for utilities
"""


import logging
log     = logging.getLogger( name=__name__ )
debug = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
info  = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )

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

# https://stackoverflow.com/questions/5189699/how-to-make-a-class-property
class ClassPropertyDescriptor( object ) :
    def __init__( self, fget, fset=None ) :
        self.fget = fget
        self.fset = fset

    def __get__( self, obj, klass=None ) :
        if klass is None :
            klass = type( obj )
        return self.fget.__get__( obj, klass )( )

    def __set__( self, obj, value ) :
        if not self.fset :
            raise AttributeError( "can't set attribute" )
        type_ = type( obj )
        return self.fset.__get__( obj, type_ )( value )

    def setter( self, func ) :
        if not isinstance( func, (classmethod, staticmethod) ) :
            func = classmethod( func )
        self.fset = func
        return self

def classproperty( func ) :
    if not isinstance( func, (classmethod, staticmethod) ) :
        func = classmethod( func )

    return ClassPropertyDescriptor( func )


#----------------------------------------------------------------------#
