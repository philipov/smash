#-- smash.sys.path

"""
path-related utility functions
"""


import logging
log = logging.getLogger( name="smash.sys.path" )
debug = print
info = print

################################
import contextlib
import os
from copy import deepcopy
from pathlib import Path
from itertools import chain



from glob import iglob, glob

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
def files_in(target_path: Path) -> list :
    files = [file for file in target_path.iterdir() if file.is_file()]
    return files

@export
def subdirectories_of( target_path: Path ) -> list :
    subdirs = [subdir for subdir in target_path.iterdir( ) if subdir.is_dir()]
    return subdirs

@export
def stack_of_files( target_path: Path, file: str ) -> list :
    lists_of_files =[ path[0] for path in \
            [list(parent.glob( file ) )
                for parent in [target_path, *target_path.parents]
            ]
            if len(path) > 0
        ]
    return lists_of_files


@export
def find_yamls(target_path:Path):
    yaml_filepaths=list()
    for file in chain( iglob( str(target_path/'*.yaml')),
                       iglob( str(target_path/'*.yml' ))
                      ):
        yaml_filepaths.append(Path(file))
    if len(glob( str(target_path/'__stop__') )) == 0 :
        yaml_filepaths = list(chain(yaml_filepaths,
                                    *( find_yamls( path ) for path in subdirectories_of(target_path) )
                                ))

    return yaml_filepaths


#----------------------------------------------------------------------#

@export
def paths2string(paths_list:list) -> str:
    """???"""
    result  = '"'
    count   = 0
    length  = len(paths_list)
    for path in paths_list:
        count += 1
        if count==length:
            result += str( path ) + ", "
        else:
            result += str( path )
    result += '"'
    return result


#----------------------------------------------------------------------#

@export
@contextlib.contextmanager
def temporary_working_directory( path: Path ) :
    """change working directory to 'path' for the duration of the context manager"""

    old_working_dir = Path( os.getcwd( ) )

    # log.debug( "dir ->", str( path ) )
    os.chdir( str( path ) )
    yield old_working_dir

    # log.debug( "dir <-", str( old_working_dir ) )
    os.chdir( str( old_working_dir ) )


#----------------------------------------------------------------------#

@export
def try_resolve( value, path:Path ) -> str:
    """"""

    #debug( "TRY RESOLVE--------", type( value ), value )
    if isinstance( value, list ):
        return value

    value = str( value )
    ### attempt to resolve paths
    result = value
    try :
    #    debug("~~~ BEGIN")
        value_as_path = Path( str(value) )
        if value_as_path.exists( ) :
            with temporary_working_directory( path ) as old_working_dir :
                result      = str( value_as_path.resolve( ) )

    except FileNotFoundError as e :
    #    debug( "File Not Found", value )
        raise FileNotFoundError( e )
    except OSError as e:
        pass

    #debug("RESOLVED", result)
    return result


#----------------------------------------------------------------------#

def fix_paths( struct, working_directory: Path ) :
    """interpret keys ending with _PATH as Path objects; resolve them to absolute paths"""
    # Todo: eliminate mutability

    if isinstance( struct, list ) :
        for item in struct :
            fix_paths( item, working_directory )
    elif isinstance( struct, dict ) :
        for (key, value) in struct.items( ) :
            if isinstance( value, dict ) :
                fix_paths( value, working_directory )
            elif isinstance( value, list ) :
                fix_paths( value, working_directory )
            elif isinstance( value, str ) and key[-5 :] == "_PATH" :
                try :
                    with temporary_working_directory( working_directory ) as old_working_dir :
                        struct[key] = Path( value ).resolve( )
                except FileNotFoundError as e :
                    print( "FILE NOT FOUND" )
                    raise FileNotFoundError( e )
    return struct

#----------------------------------------------------------------------#


# ToDo: Path-addressable Dictionary
