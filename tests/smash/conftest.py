#-- conftest.unit

"""
fixtures for module unit tests
"""

import pytest
import time
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('conftest.unit')


#----------------------------------------------------------------------#

@pytest.fixture( scope="session" )
def path_root_config(path_testdata):
    return path_testdata/'__root__.yml'


#----------------------------------------------------------------------#


@pytest.fixture( scope="session" )
def path_env00( path_testdata ) :
    return path_testdata/'env'/'00'

@pytest.fixture( scope="session" )
def path_env00_config( path_env00 ) :
    return path_env00/'__env__.yml'


@pytest.fixture( scope="session" )
def path_examples( path_env00 ) :
    return path_env00/'examples'

@pytest.fixture( scope="session" )
def path_example_daemon( path_examples ) :
    return path_examples/'start_daemon.yml'

@pytest.fixture( scope="session" )
def path_example_job( path_examples ) :
    return path_examples/'schedule_job.yml'

@pytest.fixture( scope="session" )
def path_example_task( path_examples ) :
    return path_examples/'run_task.yml'


#----------------------------------------------------------------------#

@pytest.fixture( scope="session" )
def path_app( path_testdata ) :
    return path_testdata/'pkg'/'app'

@pytest.fixture( scope="session" )
def path_app_config( path_app ) :
    return path_app/'__pkg__.yml'


#----------------------------------------------------------------------#

@pytest.fixture( scope="session" )
def path_lib( path_testdata ) :
    return path_testdata/'pkg'/'lib'

@pytest.fixture( scope="session" )
def path_lib_config( path_lib ) :
    return path_lib/'__pkg__.yml'


#----------------------------------------------------------------------#

@pytest.fixture( scope="session" )
def path_data( path_testdata ) :
    return path_testdata/'pkg'/'data'

@pytest.fixture( scope="session" )
def path_data_config( path_data ) :
    return path_data/'__pkg__.yml'


#----------------------------------------------------------------------#

@pytest.fixture( scope="session" )
def path_host( path_testdata ) :
    return path_testdata/'pkg'/'host'

@pytest.fixture( scope="session" )
def path_host_config( path_host ) :
    return path_host/'__pkg__.yml'


#----------------------------------------------------------------------#

@pytest.fixture( scope="session" )
def path_network( path_testdata ) :
    return path_testdata/'pkg'/'network'

@pytest.fixture( scope="session" )
def path_network_config( path_network ) :
    return path_network/'__pkg__.yml'


#----------------------------------------------------------------------#
