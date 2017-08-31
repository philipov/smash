#-- smash.sys.out

'''
description
'''

from contextlib import suppress

#----------------------------------------------------------------------#

from termcolor import colored
green   = lambda s : colored( s, 'green', attrs=['bold'] )
red     = lambda s : colored( s, 'red', attrs=['bold'] )
blue    = lambda s : colored( s, 'blue', attrs=['bold'] )
cyan    = lambda s : colored( s, 'cyan', attrs=['bold'] )
yellow  = lambda s : colored( s, 'yellow', attrs=['bold'] )
pink    = lambda s : colored( s, 'magenta', attrs=['bold'] )

from pprint import PrettyPrinter
_pprinter = PrettyPrinter()
pprint = _pprinter.pprint

#----------------------------------------------------------------------#

def add_pprint(cls):
    _pprinter._dispatch[cls.__repr__] = cls.__pprint__


#----------------------------------------------------------------------#

#ToDo: 'tprint' - write to local log stream and stdout

def dictprint( d ) :
    list( print( key, ':', value ) for key, value in d.items( ) )

def listprint( l ) :
    list( print( value ) for value in l )

def rprint( struct, i=0, quiet=False ) :
    #ToDo: return a string

    result = ""
    if isinstance( struct, list ) : # loop over list
        for value in struct :
            if isinstance( value, dict ) \
                    or isinstance( value, list ) : # recurse on subsequence
                result += rprint( value, i + 2, quiet )

            else :
                line = ' '*i + "- " + str( value )
                result += line + "\n"
                print( line ) if quiet is False else None

    elif isinstance( struct, dict ) : # loop over dict
        for (key, value) in struct.items( ) :
            line = ' '*i + "" + str( key ) + ": "
            result += line
            print( line, end='' ) if quiet is False else None

            if isinstance( value, dict ) \
                    or isinstance( value, list ) : # recurse on subsequence
                print( "" ) if quiet is False else None
                result += "\n"
                result += rprint( value, i + 2, quiet )

            else :
                result += str( value ) + "\n"
                print( str( value ) ) if quiet is False else None

    return result


#----------------------------------------------------------------------#

def callstr( obj ) -> str:
    with suppress(Exception):
        return str(obj())
    return str(obj)

def wrap_log_func (func, prefix='', suffix='', **static_kwargs):
    return lambda *args, **kwargs : func( callstr(prefix)+"".join( str( arg ) for arg in args )+callstr(suffix), **static_kwargs )

def logger_funcs():
    import logging
    log = logging.getLogger( name='smash.sys.config' )

    debug       = wrap_log_func( print )
    info        = wrap_log_func( print )
    warning     = wrap_log_func( print )
    error       = wrap_log_func( print )
    critical    = wrap_log_func( print )


    return debug, info, warning, error, critical


#----------------------------------------------------------------------#
