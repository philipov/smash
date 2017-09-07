

'''
integration tests for main program
'''

import shlex
import pytest
import os

#----------------------------------------------------------------------#

params_argv = list()
params_argv.append(shlex.split('run echo import time; time.sleep(5) | python -'))
params_argv.append( shlex.split( 'run echo >>>>>>>> HELLO WORLD <<<<<<<<' ) )

@pytest.mark.parametrize("argv", params_argv)
def test__main( path_env00, argv ) :

    from smash.__main__ import main
    from smash.cmdline import parse

    os.chdir( str( path_env00) )
    args    = parse(argv)
    result  = main( args )

    # assert False


#----------------------------------------------------------------------#


