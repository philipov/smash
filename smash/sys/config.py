#-- smash.sys.config

"""
manipulate configuration files
"""


import logging
log     = logging.getLogger( name=__name__ )
# debug   = lambda *a, **b : log.debug( "".join( str( arg ) for arg in a ) )
# info    = lambda *a, **b : log.info(  "".join( str( arg ) for arg in a ) )
debug = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
info  = lambda *a, **b : print( "".join( str( arg ) for arg in a ) )
# debug = lambda *a, **b : None

################################

import os
import re

from termcolor import colored

from collections import defaultdict
from collections import ChainMap
from collections import OrderedDict
from ordered_set import OrderedSet

from functools import reduce
from itertools import chain
from contextlib import suppress
from glob import iglob

from pathlib import Path

from .yaml import load as load_yaml
from .path import stack_of_files
from .path import temporary_working_directory
from .path import try_resolve
from .path import find_yamls

from . import out
from .out import debuglog
from .out import rprint, listprint, dictprint
from pprint import pprint, pformat

#----------------------------------------------------------------------#

__all__ = []

def export( obj ) :
    try :
        __all__.append( obj.__name__ )
    except AttributeError :
        __all__.append( obj.__main__.__name__ )
    return obj


#----------------------------------------------------------------------#

####################
def getdeepitem( data, keys ) :
    return reduce( lambda d, key : d.setdefault( key, OrderedDict( ) ) if not isinstance(d, list) else d[key], keys, data )


class GreedyOrderedSet(OrderedSet):
    '''OrderedSet that keeps the last value added to it instead of the first.'''

    def add( self, key ) :
        """ Add `key` as an item to this OrderedSet, then return its index.
            If `key` is already in the OrderedSet, delete it and add it again.
        """

        if key not in self.map :
            self.map[key] = len( self.items )
            self.items.append( key )
        else:
            self.discard(key)
            self.add(key)
        return self.map[key]

    append = add



#----------------------------------------------------------------------#

@export
class ConfigTree:
    """ Non-mutating (append-only) iterator over a network of configuration files with cross-tree references."""

    #----------------------------------------------------------------#
    #----------------------------------------------------------------#

    ####################
    def __init__( self, *
                  , root_file:  Path = None
                  , env_path:   Path = None
                  ) :

        self.nodes      = OrderedDict()
        self.root       = None

        self.root_filepath  = root_file
        self.env_path       = env_path

        self.out_file   = None
        self.raw_file   = None
        self._final     = False

        if root_file is not None:
            self.__add_root( root_file )


    ####################
    @classmethod
    def from_path( cls, target_path: Path  ) :
        """Find the root file for a target path, load it and its children"""
        root_file = stack_of_files( target_path, '__root__.yml' )[0]
        root_path = root_file.parents[0]

        try:
            env_path = stack_of_files( target_path, '__env__.yml')[0].parents[0]
        except IndexError as e:
            print('Warning - __env__.yml file not found. Using root node...')
            env_path = root_file.parents[0]


        self = cls( root_file=root_file, env_path=env_path )

        # todo: instead of searching for files, load files referenced by root and env, recursively
        with temporary_working_directory( root_path):
            for file in find_yamls(root_path):
                if file != self.root.filepath:
                    # todo: skip files that throw an invalid config exception
                    self.add_node(Path(file))

        self.finalize()
        return self


    ####################
    @classmethod
    def from_root( cls, root_file: Path ) :
        self = cls( root_file=root_file )
        return self


    #----------------------------------------------------------------#
    #----------------------------------------------------------------#

    def add_root(self, root_file):
        assert self.root is None
        node = self.__add_node(root_file)
        self.root = node

    def add_node(self, target_file):
        node = Config.from_yaml(target_file, tree=self)
        self.nodes[node.filepath] = node
        return node

    __add_root  = add_root
    __add_node  = add_node


    def finalize( self ) :
        self._final = True


    #----------------------------------------------------------------#

    ####################
    def __getitem__( self, filepath=None ) :
        ''' return the config node at a given filepath
            if no filepath is given, returns the root node
            if only a path is given, tries to guess the filename
        '''
        if filepath is None :
            return self.root

        with suppress( KeyError ) :
            return self.nodes[Path( filepath )]

        with suppress( KeyError ) :
            return self.nodes[Path( filepath ) / '__env__.yml']

        with suppress( KeyError ) :
            return self.nodes[Path( filepath ) / '__pkg__.yml']

        with suppress( KeyError ) :
            return self.nodes[Path( filepath ) / '__root__.yml']

        raise KeyError( filepath, 'not found in', self )


    ####################
    def __len__(self):
        return len(self.nodes)


    ####################
    def __str__(self):
        return "".join(str(s)
            for s in [
                '<', self.__class__.__name__, ' of ', self.root.__class__.__name__, ': [', len(self), '], ', 'root=', self.root.path, '>'
            ])

    __pprint__ = __str__
    __repr__ = str


    #----------------------------------------------------------------#

    @property
    def root_name( self ) :
        return self.root._yaml_data['__name__']

    @property
    def root_type( self ) :
        return self.root._yaml_data['__type__']

    @property
    def root_protocol( self ) :
        return self.root._yaml_data['__protocol__']

    @property
    def root_version( self ) :
        return self.root._yaml_data['__version__']

    @property
    def envfile( self ) :
        return '__env__.yml'

    ####################
    def find_nodes( self, pattern ) :
        results = list( )
        for (node_filepath, node) in self.nodes.items( ) :
            if re.match( pattern, str( node.name ) ) is not None :
                results.append( node )
        if len( results ) == 0 :
            results.append( self.root )
        return results

    @property
    def envlist( self ) :
        return self.find_nodes( self.envfile )

    @property
    def packagelist( self ) :
        return self.find_nodes( '__pkg__\.yml' )


    ####################
    @property
    def by_name( self ) :
        result = defaultdict( list )
        for (name, node) in self.nodes.items( ) :
            result[node.name.split( '.' )[0]].append( node )
        return result

    @property
    def by_env( self ) :
        result = dict( )
        for node in self.envlist :
            result.setdefault( node.path.name, node )
        return result

    @property
    def by_pkg( self ) :
        result = dict( )
        for node in self.packagelist :
            result.setdefault( node.path.name, node )
        return result

    def node( self, name=None ) :
        if name is None :
            return self.nodes[self.env_path / self.envfile]
        return self.nodes[name]

    @property
    def current_env( self ) :
        try:
            return self.nodes[self.env_path / self.envfile]
        except KeyError as e:
            debug('KeyError:', e)
            return self.root


    #----------------------------------------------------------------#

    def nearest_node( self, target_name:str, target_path:Path ):
        """ return the child config node for the nearest parent of the target path."""
        # Todo: perform this on the saved config structure, not the filesystem.
        for filepath in stack_of_files( target_path, target_name ):
            if filepath in self.nodes.keys():
                return filepath


    ####################]
    def subenv( self, name=None, pure=False ) :
        if not pure :
            subenv = os.environ.copy( )
        else :
            subenv = OrderedDict( )

        try :
            section_items = self.root_export.items( )
        except KeyError :
            section_items = list( )

        env_sections = list( )
        for (section_name, type) in section_items :
            if type == 'environment' :
                env_sections.append( section_name )

        print( 'sections', env_sections )

        for section_name in env_sections :
            try :
                for (key, value) in self.current_env[section_name].items( ) :
                    print( 'ENV', section_name, key, value )
                    subenv[key] = value
            except KeyError as e :
                print( "KeyError:", e )

        return subenv


    ####################]
    def write_child( self, child_name: Path ) :
        print( "BUILD CONFIG -----------" )

        config = self.nodes[child_name]

        path_config = config.rootpath / '.config' / 'smash'
        try :
            path_config.mkdir( )
        except FileExistsError as e :
            pass
        config.write( self.out_file )
        config.write( self.raw_file, raw=True )


#----------------------------------------------------------------------#


#----------------------------------------------------------------------#

# todo: a config could be in a python module instead of a yaml file

@export
class Config:
    """ A single non-mutating configuration structure
        config[section][key]
        sections may be nested within sections arbitrarily deep
        the interpretation of the keys is delegated to the ConfigSectionView
    """

    ####################
    def __init__( self, tree=None ) :

        self.name       = None
        self.path       = None
        self.filepath   = None

        self._yaml_data     = None
        self._final_cache   = OrderedDict( )

        self.tree       = tree
        self._parents   = GreedyOrderedSet()    # 'inherit' parents; always inherit from tree.root


    ####################
    @classmethod
    def from_yaml( cls, target_file: Path, tree=None ) :
        self = cls( tree=tree )
        self.load( target_file )
        return self


    ####################
    def load( self, target: Path ) :
        self.filepath   = target
        self.path       = target.parents[0]
        self.name       = target.name

        self._yaml_data  = load_yaml( target )
        # todo: validate dunder keys and raise exception if not compatible format
        if self._yaml_data is not None :
            for section_name in self._yaml_data.keys( ) :
                self._final_cache[section_name] = OrderedDict( )

        debug( out.yellow( '*' * 20 ), ' load=', self.filepath )

        if self.tree is not None :
            self.tree.nodes[self.filepath] = self


    #----------------------------------------------------------------#
    #----------------------------------------------------------------#

    def __str__( self ) :
        return "".join( str( s )
                        for s in [
                            '<', self.__class__.__name__, ': ', self.filepath, '>'
                        ] )

    __pprint__= __str__
    __repr__ = str

    ####################
    @property
    def inherits( self ) -> list :

        try :
            parent_paths = self._yaml_data['__inherit__']
            parsed_paths = ConfigSectionView( self.tree.root ).evaluate_list( '__inherit__', parent_paths )
            #todo: this means that ConfigSectionView needs refactoring
            print( 'PARSED~~~~~', parsed_paths )
        except KeyError as e :
            parsed_paths = list( )

        return parsed_paths



    @property
    def parents( self ) :
        parent_paths = self.inherits
        parents = list( )
        for parent_path in parent_paths :
            parent = self.tree.nodes[Path( parent_path )]
            parents.append( parent )
            parents.extend( parent.parents )

        return GreedyOrderedSet( chain( parents, [self.tree.root] ) )

    ####################
    @property
    def key_resolution_order( self ) :
        # todo: !!! This needs to be in order of last-duplicate -- parents follow all children
        return GreedyOrderedSet( chain( [self], self.parents ) )

    ####################
    @property
    def sections( self ) :
        section_names = set( )
        for node in self.key_resolution_order :
            for (key, section) in node.items( ) :
                if not key.startswith( '__' ) and not key.endswith( '__' ) :
                    section_names.add( key )
        return section_names

    def keys( self ) :
        kro = list( self.key_resolution_order )
        datalist = [node._yaml_data for node in kro]
        datachain = ChainMap( *datalist )
        keyview = OrderedSet( sorted( datachain.keys( ) ) )
        return keyview

    ####################
    def items( self ) -> list :
        # todo: exclude dunder keys
        return self._yaml_data.items( )

    ####################
    def setdefault( self, key, default ) :
        '''support for getdeepitem on Config object'''
        try :
            return self[key]
        except KeyError :
            return self._yaml_data.setdefault( key, default )

    ####################
    def __getitem__( self, section_name ) :
        return ConfigSectionView( self, section_name )

    ####################


#----------------------------------------------------------------------#

out.add_pprint( ConfigTree )
out.add_pprint( Config )


#----------------------------------------------------------------------#

class ConfigSectionView :
    ''' dictionary view of a config section that provides alternate indexing logic
        search config parents for keys if not found in the current one
        perform token substitution, expression evaluation, and path resolution on raw scalar values
    '''

    ####################
    def __init__( self, config:Config, *names ) :
        self.config = config
        self.section_keys = names
        self.parse_counter = 0


    ####################
    def __str__( self ) :
        return "".join( str( s ) for s in [
            '<', self.__class__.__name__, ': ', self.config.name, ' \'', self.section_keys, '\'>'
        ])

    __pprint__ = __str__
    __repr__ = str

    ####################
    def keys( self ) :
        key_union = set()
        for node in self.config.key_resolution_order :
            for key in getdeepitem(node._yaml_data, self.section_keys).keys():
                key_union.add(key)
        return list(key_union)


    def items( self ) :
        results = self.config[self.section_keys].items( )
        return results
        # for node in self.config.key_resolution_order():
        #     print(str(node))


    ####################
    def setdefault( self, key, default ) :
        ''' support for getdeepitem on Config object'''
        try :
            return self[key]
        except KeyError :
            return getdeepitem( self.config._yaml_data, self.section_keys ).setdefault( key, default )


    ####################
    def __getitem__( self, key ) :
        ''' obtain the 'flat' value of the key in the configtree, from the point of view of the current config
            if the current config contains the key, evaluate it and store it in a cache
            if the value is a list, evaluate each element of the list and return the parsed list
            if we need to look in a different node for the key, the process recurses from the point of view of that node
            paths are resolved relative to the path of the file they're defined in, so '.' means the current file's path.
            supports dictionaries inside dictionaries by returning nested ConfigSectionView objects
        '''

        # check cache
        try :
            final_value = getdeepitem( self.config._final_cache, self.section_keys )[key]
        except KeyError :
            pass
        else:
            print('else', self.config.name)
            return final_value

        # check current node
        print("find_item", self.section_keys, key)
        try:
            raw_value = getdeepitem( self.config._yaml_data, self.section_keys )[key]
        except KeyError:
            raw_value = None
        else:
            if isinstance( raw_value, dict ) :                                                  # Dict Value Found
                print( 'config_view', key )
                configview = ConfigSectionView( self.config, *self.section_keys, key )
                return configview

            elif isinstance( raw_value, list ) :                                                # List Value Found
                print( 'list' )
                parsed_list = self.evaluate_list(key, raw_value)

                print( out.cyan('~~~Cache List Result'), self.section_keys, key, parsed_list )
                getdeepitem( self.config._final_cache, self.section_keys )[key] = parsed_list   # CACHE LIST ###
                return parsed_list

            else :                                                                              # Scalar Value Found
                final_value = self.evaluate( key, raw_value )

                print( out.cyan('~~~Cache Scalar Result'), self.section_keys, key, final_value )
                getdeepitem( self.config._final_cache, self.section_keys )[key] = final_value   # CACHE VALUE ###
                return final_value

        # check parents
        print('MISSING IN', self.config.filepath, 'keys', self.section_keys)
        for node in self.config.parents:
            # print("look in parent:", node)
            if node is self.config:
                continue
            try:
                parent_value = getdeepitem( node, self.section_keys )[key]
            except KeyError:
                # print("MISSING IN ", node.filepath)
                continue
            else:
                print(out.blue('parent_value:'), self.section_keys, key, parent_value, self.config.filepath)
                return parent_value

        # not found
        raise KeyError(str(key)+' not found.')


    ####################
    def evaluate_list(self, key, raw_list):
        parsed_list = []
        for (i, value) in enumerate( raw_list ) :
            if isinstance( value, list ) or isinstance( value, dict ) :
                new_value = ConfigSectionView( self.config, *self.section_keys, key, i )
            else :
                new_value = self.evaluate( key, value )
            parsed_list.append( new_value )
        return parsed_list


    ####################
    def evaluate(self, key, value) -> str:
        ''' parse a raw value
            perform regex substitution on ${} token expressions until there are none left
            then attempt to resolve the result relative to the config file's path
        '''

        new_value=value
        total_count = 1

        while total_count > 0 :
            total_count = 0
            (new_value, count) = self.substitute( key, str(new_value) )
            total_count += count

        final_value = try_resolve(new_value, self.config.path)

        return final_value  # todo: DifferedPath


    ####################
    def substitute( self, key, value: str ) :

        total_count = 0
        count = None

        debug( 'VALUE --- ', colored( value, 'red', attrs=['bold'] ) )


        expression_replacer = self.expression_parser( key)
        (result, count)     = token_expression_regex.subn( expression_replacer, value )
        debug( "After re.subn:  ", result, " | ", count, "|", expression_replacer.counter[0] )

        total_count += expression_replacer.counter[0] + count# ToDo: Replace monkey patch with class
        debug( "Subn Result: ", result, ' after ',total_count )
        return result, total_count


    ####################
    def expression_parser( self, key ) :
        ''' factory that creates a replacement function to be used by regex subn
            process ${configpath@section:key} token expressions:
            -    key:        look up value in target node
            -    sections:   [optional] key is in a sibling section
            -    configpath: [optional] key is in a different file

            a token specifies a key that is to be looked up in a certain config node.
            If no section is specified, the same section the key is found in is searched.
            If no configpath is specified, the same file is assumed, except in the case of a self-referential key
            lookup for self-referential keys looks directly in the config's first parent.
            if configpath is specified, the parent list pseudo-chainmap behavior is still respected.
            if section or sections (section1:section2:section3) are specified, look in those sections
        '''

        counter = [0]
        def expression_replacer( matchobj ) :

            target_configpath   = matchobj.group( 'configpath' ) \
                if (matchobj.group( 'configpath' ) is not None) \
                else self.config.filepath
            target_sections     = matchobj.group( 'sections' ).split( ':' ) \
                if (matchobj.group( 'sections' ) is not None) \
                else self.section_keys
            target_key          = matchobj.group( 'key' )

            self.parse_counter += 1
            debug( '>'*20, " MATCH ", target_configpath, ' ', target_sections, ' ', target_key, ' | ', key, ' ',  self.section_keys )
            debug( matchobj.groups( ) )

            section_keys    = [*target_sections, target_key]
            node            = self.config.tree[target_configpath]

            # self-key references begin the search from the config's immediate parent
            if key == target_key \
                    and self.section_keys == target_sections \
                    and self.config.filepath == target_configpath:
                node = node.parents[0]

            result = getdeepitem(node, section_keys)
            return result

        ###
        expression_replacer.counter = counter
        return expression_replacer


#----------------------------------------------------------------------#

#todo: delayed key evaluation syntax -- causes a parent value to have its token expressions evaluated from the child's point of view
token_expression_regex = re.compile(
    r"""\${                                  # ${
            ((?P<configpath>[^${}]+?)@)?     #   configpath@         [optional]
            ((?P<sections>[^${}]+):)?        #   sections:           [optional]
            (?P<key>[^$:{}]+?)               #   key                 -required-
          }                                  #  }
    """, re.VERBOSE )




#----------------------------------------------------------------------#


