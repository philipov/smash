#-- smash.sys.plugins

"""
load plugins
"""


import logging
log = logging.getLogger( name=__name__ )
logging.basicConfig( level=logging.DEBUG )
log.debug = print
# log.debug = lambda *a, **b : None

import pkg_resources

from .out import rprint

#----------------------------------------------------------------------#

__all__ = ['plugins']

#----------------------------------------------------------------------#

def _load_plugins():
    ''' produce a dictionary of available plugin modules
    '''
    plugins = {
        entry_point.name : entry_point.load( )
        for entry_point
        in pkg_resources.iter_entry_points( 'smash.plugins' )
    }

    print('~~~~~~~~~~~ smash.sys.plugins')
    rprint(plugins)


    return plugins
plugins = _load_plugins()

#----------------------------------------------------------------------#
def _load_exporters(plugins_):
    for module_name, module in plugins.items():
        for attribute, value in module.__dict__.items():
            print('ATTRIBUTE', attribute, value)
    return dict()
exporters = _load_exporters(plugins)

print("__name__", __name__)

#----------------------------------------------------------------------#
