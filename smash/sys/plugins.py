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
from contextlib import suppress
from copy import copy

from .out import rprint
from . import out
from .export import Exporter, base_exporters

#----------------------------------------------------------------------#

__all__ = ['plugins', 'exporters']

#----------------------------------------------------------------------#
def _load_plugins():
    ''' produce a dictionary of available plugin modules
    '''
    plugins = {
        entry_point.name : entry_point.load( )
        for entry_point
        in pkg_resources.iter_entry_points( 'smash.plugins' )
    }
    return plugins
plugins = _load_plugins()


#----------------------------------------------------------------------#
def _load_exporters(plugins_):
    results = copy(base_exporters)
    for module_name, module in plugins.items():
        for attribute, value in module.__dict__.items():
            if not attribute.startswith('_'):
                with suppress(TypeError):
                    if issubclass(value, Exporter):
                        results[value.__name__]=value
    return results
exporters = _load_exporters(plugins)

print(  out.green('~~~~~~~~~~~') +' smash.sys.plugins' )
rprint( plugins )
print(  out.green('~~~~~~~~~~~') +' exporters:')
rprint( exporters )


#----------------------------------------------------------------------#
