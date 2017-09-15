#-- smash.core.config

"""
manipulate configuration files
yamlisp attempt #2
"""

#todo: separate out the yaml processing from the core config concepts; configtree should be a metaclass representing configs as classes

from powertools import AutoLogger
log     = AutoLogger()


################################

import os
import re

from collections import defaultdict
from collections import ChainMap
from collections import OrderedDict
from collections import namedtuple
from collections import deque
from ordered_set import OrderedSet

from functools import reduce
from itertools import chain
from contextlib import suppress


from pathlib import Path

from ..util.yaml import load as load_yaml
from ..util.path import stack_of_files
from ..util.path import temporary_working_directory
from ..util.path import try_resolve
from ..util.path import find_yamls

from ..util import out
from powertools.print import listprint, dictprint, rprint, pprint, pformat

from smash.core.constants import CONFIG_PROTOCOL

from powertools import export

#----------------------------------------------------------------------#

KEY_RESOLUTION_ORDER    = None
CURRENT_NODE            = None

####################
def getdeepitem( data, keys, kro=() ) :
    return reduce( lambda d, key :
                   d.setdefault( key, OrderedDict( ), kro=kro ) if isinstance(d, ConfigSectionView)
              else d.setdefault( key, OrderedDict( ) )          if not isinstance(d, list)
              else d[key],
                   keys, data )



####################
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

# todo: a config could be in a python module instead of a yaml file

@export
class Config:
    """ A single non-mutating configuration structure
        config[section][key]
        sections may be nested within sections arbitrarily deep
        the interpretation of the keys is delegated to the ConfigSectionView
    """

    class ProtocolError(Exception):
        '''Yaml file did not have the correct protocol'''

    class EmptyFileWarning(Exception):
        '''May wish to ignore blank config files'''

    class SubstitutionKeyNotFoundError(Exception):
        '''expression token contained a key whose value could not be found during regex substitution'''

    class TokenExpressionError(Exception):
        '''$ tokens are scalar substitutions, @ tokens are sequence extensions'''


    ####################
    def __init__( self, tree=None ) :

        self.filename   = None
        self.path       = None
        self.filepath   = None

        self._yaml_data     = None
        self._final_cache   = OrderedDict( )

        self.tree       = tree

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
        self.filename   = target.name

        self._yaml_data  = load_yaml( target )
        # todo: validate magic keys and immediately raise exception if not a compatible format

        if self._yaml_data is None:
            raise Config.EmptyFileWarning(self.filepath)

        for section_name in self._yaml_data.keys( ) :
            self._final_cache[section_name] = OrderedDict( )

        try:
            assert self.protocol == CONFIG_PROTOCOL
        except KeyError as e:
            raise Config.ProtocolError('Missing __protocol__', str(self))
        except AssertionError as e:
            raise Config.ProtocolError('Protocol version mismatch')

        log.print( out.yellow( '*' * 20 ), ' load=', self.filepath )

        print('parents:',self.__inherit__)

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

    @property
    def name( self ) :
        return self._yaml_data['__name__']

    @property
    def type( self ) :
        return self._yaml_data['__type__']

    @property
    def protocol( self ) :
        return self._yaml_data['__protocol__']

    @property
    def version( self ) :
        return self._yaml_data['__version__']

    @property
    def is_pure( self ) :
        with suppress(KeyError):
            return bool(self._yaml_data['__pure__'])
        return True


    ####################
    @property
    def __inherit__( self ) -> list :
        ''' this node's immediate parents, a list of keys (paths) to find them in the configtree'''

        try :
            parent_paths = self._yaml_data['__inherit__']
            # print( 'PARSED~~~~~', parent_paths )
            parsed_paths = ConfigSectionView( self.tree.root ).evaluate_list( '__inherit__', parent_paths, (self.tree.root,) )
            #todo: this means that ConfigSectionView needs refactoring
        except KeyError as e :
            # print("KeyError",  e, self)
            parsed_paths = list( )

        return parsed_paths

    @property
    def parents( self ) :
        ''' the full ordered set of all parent nodes, after recursive linearization'''

        parent_paths    = self.__inherit__
        parents         = list( )
        for parent_path in parent_paths :
            parent      = self.tree.nodes[Path( parent_path )]
            parents.append( parent )
            parents.extend( parent.parents )

        return GreedyOrderedSet( chain( parents, [self.tree.root] ) )


    ####################
    @property
    def key_resolution_order( self ) :
        return GreedyOrderedSet( chain( [self], self.parents ) )


    ####################
    def __getitem__( self, section_name ) :
        return ConfigSectionView( self, section_name )

    ####################
    def setdefault( self, key, default ) :
        ''' support for getdeepitem on Config object'''
        try :
            return self[key]
        except KeyError :
            return self._yaml_data.setdefault( key, default )


    ####################
    @property
    def sections( self ) :
        section_names = GreedyOrderedSet( )
        for node in self.key_resolution_order :
            for (key, section) in node.items( ) :
                if not key.startswith( '__' ) and not key.endswith( '__' ) :
                    section_names.add( key )
        return section_names

    def keys( self ) :
        kro = list( self.key_resolution_order )
        datalist    = [node._yaml_data for node in kro]
        datachain   = ChainMap( *datalist )
        keyview     = OrderedSet( sorted( datachain.keys( ) ) )
        return keyview

    ####################
    def items( self ) -> list :
        # todo: exclude dunder keys
        return self._yaml_data.items( )


    ####################

    @property
    def __export__( self ):
        ''' parse the export dictionary for this node and return it'''

        # todo: BUG! why does 'pkg' or 'env' in the sections list evaluate to a path?
        try :
            export_items    = self['__export__'].items()
            parsed_dict     = export_items #OrderedDict()
            #parsed_paths    = ConfigSectionView( self.tree.root, '__export__' ).evaluate_list( '__exports__', export_dict )
            #todo: this means that ConfigSectionView needs refactoring
            # print( out.green('PARSED~~~~~'), parsed_dict )
        except KeyError as e :
            parsed_dict = OrderedDict()

        # print( out.white( '_export' ), parsed_dict )
        return parsed_dict

    @property
    def exports(self) -> OrderedDict:
        ''' a dictionary of exporter names mapped to a list of (output names, list of section keys)'''

        result = OrderedDict()
        for node in self.key_resolution_order :
            #print( out.cyan( 'node:' ), node)
            for destination, speclist in node.__export__:
                parsed_destination = ConfigSectionView(self, 'path').evaluate('__destination__', destination)
                assert len(speclist) > 1
                exporter_name   = speclist[0]
                export_subtrees = OrderedSet(speclist[1:])
                # print( out.white( '    export' ), destination, out.white('|'), exporter_name, out.white( '|' ), export_subtrees )

                if exporter_name not in result:
                    result[exporter_name] = OrderedDict()
                if parsed_destination not in result[exporter_name]:
                    result[exporter_name][parsed_destination] = export_subtrees
                else:
                    result[exporter_name][parsed_destination] |= export_subtrees

        return result


#----------------------------------------------------------------------#

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
        self.resultlist = list()


    ####################
    def __str__( self ) :
        return "".join( str( s ) for s in [
            '<', self.__class__.__name__, ': ', self.config.filepath, ' \'', self.section_keys, '\'>'
        ])

    __pprint__ = __str__
    __repr__ = str


    ####################
    def keys( self ) :
        '''list of keys for the current subtree of the config'''

        key_union = GreedyOrderedSet( )
        for key in getdeepitem( self.config._yaml_data, self.section_keys ).keys( ) :
            # print( out.green( 'key:' ), key )
            key_union.add( key )
        return list( key_union )

    def items( self ) :
        '''key-value tuples for the current subtree only, with values resolved'''

        # print( out.blue( 'items' ), self.section_keys )
        return list( map(
            lambda key : (
                key,
                getdeepitem( self.config, [*self.section_keys, key] )
            ),
            self.keys( )
        ) )


    ####################
    def allkeys( self ) :
        '''get the union of keys for all nodes in the key resolution order'''

        key_union = GreedyOrderedSet()
        for node in self.config.key_resolution_order :
            # print(out.cyan('node:'), node, self.section_keys, '\n',
            #       getdeepitem( node._yaml_data, self.section_keys ))
            for key in getdeepitem(node._yaml_data, self.section_keys).keys():
                # print(out.green('    key:'), key)
                key_union.add(key)
        #     print( out.green( '\n------------------------------------' ))
        # print(out.cyan( '\n------------------------------------' ))
        return list(key_union)

    def allitems( self ) :
        '''same as items, but uses allkeys method'''

        # print( out.blue( 'allitems' ), self.section_keys )
        return list( map(
            lambda key : (
                key,
                getdeepitem( self.config, [*self.section_keys, key], self.config.key_resolution_order )
            ),
            self.allkeys( )
        ) )


    ####################
    def setdefault( self, key, default, kro ) :
        ''' support for getdeepitem on Config object'''
        # print( out.blue( "-----------------------------" ), 'begin setdefault', self.config, self.section_keys, out.white( key ) )
        try :
            return self._getitem(key, kro)
        except KeyError :
            return getdeepitem( self.config._yaml_data, self.section_keys, kro ).setdefault( key, default )


    ###################
    def __getitem__( self, key ) :
        ''' obtain the 'flat' value of the key in the configtree, from the point of view of the current config
            if the current config contains the key, evaluate it and store it in a cache
            if the value is a list, evaluate each element of the list and return the parsed list
            if we need to look in a different node for the key, the process recurses from the point of view of that node
            paths are resolved relative to the path of the file they're defined in, so '.' means the current file's path.
            supports dictionaries inside dictionaries by returning nested ConfigSectionView objects
        '''
        # print(out.blue("-----------------------------"), 'begin __getitem__', self.config, out.white(key))
        return self._getitem(key, self.config.key_resolution_order)

    def _getitem( self, key, kro) :

        ### check cache
        try :
            final_value = getdeepitem( self.config._final_cache, self.section_keys )[key]
        except KeyError :
            pass
        else:
            # print('else', self.config.name)
            return final_value

        ### construct the current state of the inheritence chain
        if len(kro) == 0:
            pruned_kro = self.config.parents
        else:
            # print(out.red("PRUNE KRO"))
            # listprint(kro)
            # print(out.red('---'), self.config)
            pruned_kro = deque( kro )
            try:
                while pruned_kro.popleft( ) != self.config : pass
            except IndexError:
                pruned_kro = (self.config.tree.root,)
            # listprint(pruned_kro)
            # print( out.red( '--- pruned' ) )


        ### check current node
        # print( out.pink( 'CHECK SELF' ), self.config.filepath, 'keys', self.section_keys, out.white( key ) )
        try:
            raw_value = getdeepitem( self.config._yaml_data, self.section_keys )[key]
        except KeyError:
            raw_value = None
        else:
            if isinstance( raw_value, dict ) :                                                  # Dict Value Found
                # print( 'config_view', key )
                configview = ConfigSectionView( self.config, *self.section_keys, key )
                return configview

            elif isinstance( raw_value, list ) :                                                # List Value Found
                # print( 'list' )
                parsed_list = self.evaluate_list(key, raw_value, kro=pruned_kro)

                # print( out.cyan('~~~Cache List Result'), self.section_keys, key, self.config , parsed_list)
                getdeepitem( self.config._final_cache, self.section_keys)[key] = parsed_list   # CACHE LIST ###
                return parsed_list

            else :                                                                              # Scalar Value Found
                final_value = self.evaluate( key, raw_value , kro=pruned_kro)

                # print( out.cyan('~~~Cache Scalar Result'), self.section_keys, key, final_value )
                getdeepitem( self.config._final_cache, self.section_keys )[key] = final_value   # CACHE VALUE ###
                return final_value


        ### check parents
        # print(out.pink('CHECK PARENTS'), self.config.filepath, 'keys', self.section_keys, out.white(key))
        # print('parents')
        # listprint(self.config.parents)
        # print('kro')
        # listprint(pruned_kro )
        for node in self.config.parents:
            # print("look in parent:", node)
            if node is self.config:
                continue
            try:
                parent_value = getdeepitem( node, self.section_keys, pruned_kro )._getitem( key, kro )
            except KeyError:
                # print("MISSING IN ", node.filepath)
                continue
            else:
                # print(out.blue('parent_value:'), self.section_keys, key, parent_value, self.config.filepath)
                return parent_value

        # not found
        # print('__getitem__', key, out.red('|'), self.config, out.red( '|' ),self.section_keys)
        raise KeyError(str(key)+' not found.')


    ####################
    def evaluate_list(self, key, raw_list, kro):
        ''' evaluate each element of the list, and return the list of parsed values '''
        parsed_list = []
        # print(out.yellow('------------'), 'EVALUATE LIST', raw_list)
        # listprint(kro)
        for (i, value) in enumerate( raw_list ) :
            if isinstance( value, list ) or isinstance( value, dict ) :
                new_value = ConfigSectionView( self.config, *self.section_keys, key, i )
            else :
                new_value = self.evaluate( key, value, listeval=True, kro=kro )
                try :
                    resultlist = self.resultlist.pop( )
                    # print( "RESULTLIST:", resultlist )
                    parsed_list.extend(resultlist)
                    continue
                except IndexError as e :
                    pass

            parsed_list.append( new_value )
        return parsed_list


    ####################
    def evaluate(self, key, value, listeval=False, kro=()) -> str:
        ''' parse a raw value
            perform regex substitution on ${} token expressions until there are none left
            then attempt to resolve the result relative to the config file's path
        '''

        new_value=value
        total_count = 1
        # print(out.green('EVALUATE:'), key, value, self)

        while total_count > 0 :
            total_count = 0
            (new_value, count) = self.substitute( key, str(new_value), listeval=listeval, kro=kro )
            total_count += count

        with temporary_working_directory(self.config.path):
            final_value = try_resolve(new_value, self.config.path)

        return final_value  # todo: DifferedPath


    ####################
    def substitute( self, key, value: str, listeval=False, kro=() ) :
        ''' responsible for running a single regex substitute
        '''
        total_count = 0
        count = None

        # log.debug( 'VALUE --- ', colored( value, 'red', attrs=['bold'] ) )
        expression_replacer = self.expression_parser( key, listeval=listeval, kro=kro)
        try:
            (result, count)     = token_expression_regex.subn( expression_replacer, value )
        except TypeError as e: # todo: handle this TypeError inside expression_replacer
            print(out.red('SUBSTITUTE'), key, value, self)
            raise e
        # log.debug( "After re.subn:  ", result, " | ", count, "|", expression_replacer.counter[0] )

        total_count += expression_replacer.counter[0] + count# ToDo: Replace monkey patch with class
        # log.debug( "Subn Result: ", result, ' after ',total_count )

        return result, total_count


    ####################
    def expression_parser( self, key, kro=(), listeval=False ) :
        ''' factory that creates a replace function to be used by regex subn
            process ${configpath::section:key} token expressions:
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

            token = matchobj.group('token')
            target_configpath   = matchobj.group( 'configpath' ) \
                if (matchobj.group( 'configpath' ) is not None) \
                else self.config.filepath
            if target_configpath == 'ENV':
                target_configpath = self.config.tree.env.filepath
            target_sections     = matchobj.group( 'sections' ).split( ':' ) \
                if (matchobj.group( 'sections' ) is not None) \
                else self.section_keys
            target_key          = matchobj.group( 'key' )

            self.parse_counter += 1
            # log.info( '>'*20, " MATCH ", target_configpath, ' ', target_sections, ' ', target_key, ' | ', key, ' ',  self.section_keys )
            # listprint(kro)
            # print("value", out.green(matchobj.group(0)))
            # print('-----------')

            # log.debug( matchobj.groups( ) )

            section_keys    = [*target_sections, target_key]
            node            = self.config.tree[target_configpath]

            ### self-key references begin the search from the config's immediate parent
            if key == target_key \
            and self.section_keys == target_sections \
            and self.config.filepath == target_configpath:
                node = kro[0]

            result = getdeepitem(node, section_keys, kro)

            # print(out.cyan("subn result:"), result, out.cyan('|'), key, out.cyan( '|' ), matchobj.group(0))
            if isinstance(result, OrderedDict) and len(result) == 0:
                raise Config.SubstitutionKeyNotFoundError(''.join(str(s) for s in [
                    'Could not find ', target_configpath, '::', target_sections,':', target_key,
                    ' for inserting into ', self.config.filepath, '::', self.section_keys,':', key,
                ]))
            elif isinstance(result, list) and matchobj.group(0) == matchobj.string and listeval and token == '@':
                ### WARNING: use a hack to return a list out from the regex substitute
                ### so we can later use it to extend a list we're substituting into
                # log.info(out.blue('*'*30), 'LIST INSERT' )
                self.resultlist.append(result)
            elif not isinstance(result, str):
                raise TypeError(' '.join(str(s) for s in [
                    "Can't substitute non-scalar result", namedtuple('_', ['section', 'key', 'result'


                                                                           ])
                                                            (target_sections, target_key, result),
                    '\n\tin', namedtuple( '_', ['section', 'key', 'value'] )
                                            (self.section_keys, key, matchobj.string)
                ]))
            elif token == '@':
                raise Config.TokenExpressionError('@ tokens may only be used to extend other sequences')
            return str(result)

        ###
        expression_replacer.counter = counter

        return expression_replacer


#----------------------------------------------------------------------#

#todo: delayed key evaluation syntax -- causes a parent value to have its token expressions evaluated from the child's point of view
    # ^ this is achieved in part by using the ENV configpath keyword

token_expression_regex = re.compile(
    r"""(   (?P<token>[$@])
          {                                  # ${
            ((?P<configpath>[^${}]+?)::)?     #   configpath@         [optional]
            ((?P<sections>[^${}]+):)?        #   sections:           [optional]
            (?P<key>[^$:{}]+?)               #   key                 -required-
          })                                  #  }
    """, re.VERBOSE )


#----------------------------------------------------------------------#

#----------------------------------------------------------------------#

@export
class ConfigTree :
    """ container for a network of configuration files with chainmap-like behavior.
        config files may have other config files as parents.
        values may contain token expressions to be substituted with the value of a different key
        if only the key is specified, the same section and the same file are assumed
        if a section:key is not in the config file, look in the parents.
        all config files implicitly use the root node of the config filesystem as a parent.
        token expressions may refer to section:keys in any file in the configtree.
        ENV is a keyword that may be used as the filename for a token to refer to the current virtual environment's config
    """

    #----------------------------------------------------------------#
    #----------------------------------------------------------------#

    class NotFinalizedError(Exception):
        '''configtree should be finalized for writing before being used'''

    ####################
    def __init__( self, *
                  , root_file: Path = None
                  , env_path: Path = None
                  ) :

        self.nodes = OrderedDict( )
        self.root = None

        self.root_filepath = root_file
        self.env_path = env_path

        self.out_file = None
        self.raw_file = None
        self._final = False

        if root_file is not None :
            self.__add_root( root_file )


    ####################
    @classmethod
    def from_path( cls, target_path: Path ) :
        """ Find the root file for a target path, load it and its children. """
        try:
            root_file = stack_of_files( target_path, '__root__.yml' )[0]
            root_path = root_file.parents[0]
        except IndexError as e:
            raise FileNotFoundError("Could not find '__root__.yml' file in <" +str(target_path)+ ">, or inside any parent directory")

        try :
            env_path = stack_of_files( target_path, '__env__.yml' )[0].parents[0]
        except IndexError as e :
            print( 'Warning - __env__.yml file not found. Using root node...' )
            env_path = root_file.parents[0]

        self = cls( root_file=root_file, env_path=env_path )

        # todo: instead of searching for files, load files referenced by root and env, recursively
        with temporary_working_directory( root_path ) :
            for file in find_yamls( root_path ) :
                if file != self.root.filepath :
                    # todo: skip files that throw an invalid config exception
                    self.add_node( Path( file ) )

        self.finalize( )
        return self


    ####################
    @classmethod
    def from_root( cls, root_file: Path ) :
        self = cls( root_file=root_file )
        return self


    #----------------------------------------------------------------#
    #----------------------------------------------------------------#

    def add_root( self, root_file ) :
        assert self.root is None
        node = self.__add_node( root_file )
        self.root = node

    def add_node( self, target_file ) :
        try:
            node = Config.from_yaml( target_file, tree=self )
            self.nodes[node.filepath] = node
            return node
        except Config.EmptyFileWarning as e:
            print('Config.EmptyFileWarning:', e)
        except Config.ProtocolError as e:
            print('Config.ProtocolError:', e)

    __add_root = add_root
    __add_node = add_node

    def finalize( self ) :
        self._final = True

    @property
    def final( self ) :
        return self._final


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
            return self.nodes[Path( filepath ) / '3.yml']

        with suppress( KeyError ) :
            return self.nodes[Path( filepath ) / '__pkg__.yml']

        with suppress( KeyError ) :
            return self.nodes[Path( filepath ) / '__root__.yml']

        raise KeyError( filepath, 'not found in', self )

    ####################
    def __len__( self ) :
        return len( self.nodes )

    ####################
    def __str__( self ) :
        return "".join( str( s ) for s in [
                '<', self.__class__.__name__, ' of ', self.root.__class__.__name__,
                ': [', len( self ), '], root=', self.root.path if self.root is not None else 'None', '>'
            ] )

    __pprint__ = __str__
    __repr__ = str


    #----------------------------------------------------------------#

    @property
    def envfile( self ) :
        return '__env__.yml'

    ####################
    def find_nodes( self, pattern ) :
        results = list( )
        for (node_filepath, node) in self.nodes.items( ) :
            if re.match( pattern, str( node.filename ) ) is not None :
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
            result[node.filename.split( '.' )[0]].append( node )
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
    def env( self ) -> Config :
        try :
            return self.nodes[self.env_path / self.envfile]
        except KeyError as e :
            log.debug( 'KeyError:', e )
            return self.root


    #----------------------------------------------------------------#

    def nearest_node( self, target_name: str, target_path: Path ) :
        """ return the child config node for the nearest parent of the target path."""
        # Todo: perform this on the saved config structure, not the filesystem.
        for filepath in stack_of_files( target_path, target_name ) :
            if filepath in self.nodes.keys( ) :
                return filepath



#----------------------------------------------------------------------#

out.add_pprint( ConfigTree )
out.add_pprint( Config )


#----------------------------------------------------------------------#
