

'''
unit tests
'''

import os

#----------------------------------------------------------------------#

from pathlib import Path
def test__path( ) :
    from pathlib import Path

    path = Path( "./server.locator" )

    # assert False


#----------------------------------------------------------------------#

def test__temporary_working_directory( path_env00 ) :
    from smash.utils.path import temporary_working_directory

    os.chdir( str( Path( '/' ) ) )
    cwd = Path( os.getcwd( ) )
    assert cwd != path_env00
    with temporary_working_directory( path_env00 ) as old_working_dir :
        new_cwd = Path( os.getcwd( ) )
        assert old_working_dir == cwd
        assert new_cwd == path_env00

    assert cwd != path_env00

    # assert False


#----------------------------------------------------------------------#

def test__files_in( path_env00 ):
    from smash.utils.path import files_in

    print( path_env00 )
    for file in files_in( path_env00 ):
        print('file:',file)

    # assert False


def test__subdirectories_of( path_testdata ) :
    from smash.utils.path import subdirectories_of

    print( path_testdata )
    for directory in subdirectories_of( path_testdata ):
        print( 'directory:', directory )

    # assert False


def test__stack_of_files( path_env00 ) :
    from smash.utils.path import stack_of_files

    print( path_env00 )
    for file in stack_of_files( path_env00, "*.*" ) :
        print( 'files:', file )

    # assert False


#----------------------------------------------------------------------#

def test__find_yamls( path_testdata ):
    '''presense of '__stop__' file should prevent searching in 'deep' directory'''
    from smash.utils.path import find_yamls

    for filepath in find_yamls( path_testdata ) :
        print( 'yaml: ', filepath )
        assert filepath.parents[0].name != 'deep'

    # assert False


#----------------------------------------------------------------------#
