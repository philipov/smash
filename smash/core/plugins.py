#-- smash.core.plugins

"""
load plugins
"""

from powertools import AutoLogger
log = AutoLogger()
from powertools import export

import pkg_resources
from copy import copy
from contextlib import suppress

from ..util import out
from powertools.print import rprint

#----------------------------------------------------------------------#

################################
def _load_plugins():
    ''' produce a dictionary of available plugin modules '''
    plugin_modules = {
        entry_point.name : entry_point.load( )
        for entry_point
        in pkg_resources.iter_entry_points( 'smash.plugins' )
    }
    return plugin_modules

################################
def _select_class( cls, base ):
    ''' scan all modules and pull out a name mapping of subclasses of the given type
        and adds it to the built-in subclasses
    '''
    global plugin_modules
    results = copy(base)
    for module_name, module in plugin_modules.items( ):
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
from .env import Environment, builtin_environment_types


__all__     = [
    'plugin_modules',
    'report_plugins',

    'exporter',
    'environment_type',
    'template',

    'package_type',
    'package',
    'tool',
    'handler',
]


plugin_modules      = _load_plugins()

environment_types   = _select_class( Environment,       builtin_environment_types )
templates           = _select_class( InstanceTemplate,  builtin_templates )
package_types       = _select_class( PackageType,       builtin_package_types )

packages            = _select_class( Package,           builtin_packages )
tools               = _select_class( Tool,              builtin_tools )
exporters           = _select_class( Exporter,          builtin_exporters )
handlers            = _select_class( Handler,           builtin_handlers )


#----------------------------------------------------------------------#

@export
def report_plugins():
    print(  out.green('~~~~~~~~~~~'), out.pink(__name__ ))
    rprint( plugin_modules )

    print( out.green( '~~~~~~~~~~~' ) + out.pink(' environment types:' ))
    rprint( environment_types )

    print( out.green( '~~~~~~~~~~~' ) + out.pink(' instance templates:' ) )
    rprint( templates )

    print( out.green( '~~~~~~~~~~~' ) + out.pink(' package types:' ) )
    rprint( package_types )

    print( out.green( '~~~~~~~~~~~' ) + out.pink(' packages:' ))
    rprint( packages )

    print( out.green( '~~~~~~~~~~~' ) + out.pink(' tools:' ))
    rprint( tools )

    print( out.green( '~~~~~~~~~~~' ) + out.pink(' exporters:' ) )
    rprint( exporters )

    print( out.green( '~~~~~~~~~~~' ) + out.pink(' handlers:' ))
    rprint( handlers )

    print( out.green( '~~~~~~~~~~~\n' ) )

#----------------------------------------------------------------------#

def plugin_decorator_template(cls, collection):
    def plugin_decorator_factory(key):
        '''decorator factory for registering plugins'''
        def plugin_decorator(obj):
            assert type(obj) == cls
            collection[key] = obj
            return obj
        return plugin_decorator
    return plugin_decorator_factory

environment_type    = plugin_decorator_template( Environment,       environment_types )
template            = plugin_decorator_template( InstanceTemplate,  templates )
packages_type       = plugin_decorator_template( PackageType,       package_types )

package             = plugin_decorator_template( Package,           packages )
tool                = plugin_decorator_template( Tool,              tools )
exporter            = plugin_decorator_template( Exporter,          exporters )
handler             = plugin_decorator_template( Handler,           handlers )

#----------------------------------------------------------------------#
