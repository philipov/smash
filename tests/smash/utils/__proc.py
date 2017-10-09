

'''
unit tests
'''

import pytest
import psutil

#----------------------------------------------------------------------------------------------#

# ToDo: don't run this test if --fast is enabled

def test__execute_command():
    """
        run a python process in a shell
        check that the shell is dead, but the python process is still running
        kill the python process
        """
    from smash.util.proc import execute
    from smash.util.proc import kill_all

    command_string = "echo import time; time.sleep(5) | python -"
    (parent, children) = execute( command_string )

    print(parent)
    print(children)
    with pytest.raises(psutil.NoSuchProcess):
        proc = psutil.Process(parent)
    for pid in children:
        proc = psutil.Process(pid)
    kill_all(children)

    # assert False


#----------------------------------------------------------------------------------------------#
