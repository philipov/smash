

'''
test for list evaluation without using testing framework
'''

#----------------------------------------------------------------------------------------------#


from smash.core.config import ConfigTree
from smash.core.config import Config
from smash.core.config import getdeepitem
from smash.util.out import listprint
from smash.util import out
from collections import OrderedDict
from pathlib import Path

path = Path('tests/testdata/env/00' ).resolve()
print('path', path)
configs = ConfigTree.from_path(path)


print( out.pink('\n>>>>>>>>> PATH/ROOT'), configs.env['path']['ROOT'] )

# print(getdeepitem(configs.current_env._yaml_data, ['__inherit__']))
print( out.pink( '\n>>>>>>>>> configs.env' ), configs.env )
print('')
listprint( configs.env.parents )

lib_key     = Path(configs.env['pkg']['LIB'])
print( out.pink( '\n>>>>>>>>> lib_key' ), lib_key )

lib_config  = configs[lib_key]
print( out.pink( '\n>>>>>>>>> lib_config' ), lib_config )
# config_env  = configs[]

lib_config = configs[ Path(configs.env['pkg']['LIB']) ]

print( '' )
lib_exports = lib_config['__export__']
print( out.pink( '>>>>>>>>> lib_exports' ), lib_exports )

print('')
exports_keys = lib_exports.keys()
print( out.pink( '>>>>>>>>> lib_exports.keys' ), exports_keys )

print( '' )
exports_items = lib_exports.items()
print( out.pink( '>>>>>>>>> lib_exports.items' ), exports_items )

#----------------------------------------------------------------------------------------------#

