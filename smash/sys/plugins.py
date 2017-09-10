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

from ..utils import out
from ..utils.out import rprint


#----------------------------------------------------------------------#

################################
def _load_plugins():
    ''' produce a dictionary of available plugin modules '''
    plugins = {
        entry_point.name : entry_point.load( )
        for entry_point
        in pkg_resources.iter_entry_points( 'smash.plugins' )
    }
    return plugins

################################
def _select_class( cls, base ):
    ''' scan all modules and pull out a name mapping of subclasses of the given type
        and adds it to the built-in subclasses
    '''
    global plugins
    results = copy(base)
    for module_name, module in plugins.items():
        for attribute, value in module.__dict__.items():
            if not attribute.startswith('_'):
                with suppress(TypeError):
                    if issubclass(value, cls):
                        results[value.__key__]=value
    return results


#----------------------------------------------------------------------#

from .exporter import Exporter, builtin_exporters
from .handler import Handler, builtin_handlers
from .tool import Tool, builtin_tools

from .instance import InstanceTemplate, builtin_templates
from .pkg import PackageType, builtin_package_types
from .pkg import Package, builtin_packages
from .env import Environment, builtin_environments


__all__     = ['plugins',

               'exporters',
               'environments',
               'templates',

               'package_types',
               'packages',
               'tools',
               'handlers']


plugins         = _load_plugins( )

exporters       = _select_class( Exporter, builtin_exporters )
environments    = _select_class( Environment, builtin_environments )
templates       = _select_class( InstanceTemplate, builtin_templates )

package_types   = _select_class( PackageType, builtin_package_types )
packages        = _select_class( Package, builtin_packages )
tools           = _select_class( Tool, builtin_tools )
handlers        = _select_class( Handler, builtin_handlers )


#----------------------------------------------------------------------#

def report_plugins():
    print(  out.green('~~~~~~~~~~~'), out.pink(__name__ ))
    rprint( plugins )

    print(  out.green('~~~~~~~~~~~') + out.pink(' exporters:'))
    rprint( exporters )

    print( out.green( '~~~~~~~~~~~' ) + out.pink(' environments:' ))
    rprint( environments )

    print( out.green( '~~~~~~~~~~~' ) + out.pink(' templates:' ))
    rprint( templates )

    print( out.green( '~~~~~~~~~~~' ) + out.pink(' packages:' ))
    rprint( packages )

    print( out.green( '~~~~~~~~~~~' ) + out.pink(' tools:' ))
    rprint( tools )

    print( out.green( '~~~~~~~~~~~' ) + out.pink(' handlers:' ))
    rprint( handlers )
    print( out.green( '~~~~~~~~~~~\n' ) )


#----------------------------------------------------------------------#

print('plugins')
