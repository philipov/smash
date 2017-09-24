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
from itertools import starmap
from contextlib import suppress


from pathlib import Path

from ..util.yaml import load as load_yaml
from ..util.path import stack_of_files
from ..util.path import temporary_working_directory
from ..util.path import try_resolve
from ..util.path import find_yamls
from . import platform

from powertools import term
from powertools.print import listprint, dictprint, rprint, pprint, pformat, add_pprint

from smash.core.constants import CONFIG_PROTOCOL

from powertools import export

#----------------------------------------------------------------------#

# todo: move this general stuff to powertools

####################
def getdeepitem( data, keys, kro=() ) :
    ''' convert nested index access to a list of keys
        supports passing along the key resolution order for configsectionview lookups
    '''
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

def name( obj ) -> str :
    ''' easier access to object name '''
    return str( obj.__name__ )

def qualname( obj: object ) -> str :
    ''' module and qualified object name '''
    return f'{obj.__module__}.{obj.__qualname__}'


#----------------------------------------------------------------------#

# todo: a config could be in a python module instead of a yaml file

@export
class Config:
    ''' A single configuration structure expressed as arbitarily nested dictionaries and lists
        config[section][key]
        sections may be nested within sections arbitrarily deep
        config[section1][section2][key]
        the interpretation of the keys is delegated to the ConfigSectionView
    '''

    class ProtocolError(Exception):
        ''' Yaml file did not have the correct protocol '''

    class EmptyFileWarning(Exception):
        ''' May wish to ignore blank config files '''

    class SubstitutionKeyNotFoundError(Exception):
        ''' expression token contained a key whose value could not be found during regex substitution '''

    class TokenExpressionError(Exception):
        ''' $ tokens are scalar substitutions, @ tokens are sequence extensions '''

    class TokenRecursionError(Exception):
        ''' RecursionError occured while performing token substitution '''

    class InheritSelfError(Exception):
        ''' config is its own parent '''
    class InheritLoopError(Exception):
        ''' config has a parent whose parent is config '''

    class ParentNotFound(Exception):
        ''' filepath in __inherit__ list could not be found '''

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

        self.filepath   = target.resolve()
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

        log.dinfo( ' Config.load = ', term.yellow(self.filepath) )

        #print( 'parents:', self.__inherit__ )

        # todo: straighten out this manual addition of self to the configtree
        if self.tree is not None :
            self.tree.nodes[self.filepath] = self

        self.load_parents()
        log.info(term.yellow('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~done: '), self.filepath,'\n')

    def load_parents(self):
        log.dinfo( 'load_parents ',term.dyellow(self.filepath), ' ', self.__inherit__)
        for path in map( lambda p: Path(p).resolve(), self.__inherit__ ):
            log.dinfo( term.pink('inherit_path: '), path)
            if not path.exists():
                raise Config.ParentNotFound(
                    '\n'+term.dcyan('Config:')+ f' {str(self.filepath)}'
                   +'\n'+term.dcyan('Parent:')+ f' {str(path)}'
                   +''   # raise Config.ParentNotfound
                )
            if path not in self.tree.nodes:

                self.tree.add_node(path)
                self.tree.nodes[path].load_parents()


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
        ''' compute this node's immediate parents from the config's __inherit__ list
            a value in the list may either be a string or a dictionary
            if it is a string, it refers to the path of a prante config file
            if dictionary, the keys must be Platform names,
                and the values are parent config file paths
        '''
        # todo: ConfigSectionView needs refactoring

        ### try to get the raw __inherit__ list
        try :
            parent_paths = self._yaml_data['__inherit__']
            # log.info( term.blue( 'parent paths: ' ), parent_paths )
        except KeyError as e :
            parent_paths = list()
        except TypeError as e:
            parent_paths = list()

        ### get the platform-specific import strings from dictionary values
        platform_paths = list()
        for path in parent_paths:
            try:
                platform_paths.append(
                    platform.choose( path )
                    if isinstance( path, dict )
                    else path
                )
            except platform.MissingKeyError as e:
                log.info( term.red('Warning: '), f'{qualname(type(e))}( {e} )' )

        # log.info( term.blue( 'platform paths: ' ), platform_paths )

        ### evaluate tokens in resulting strings
        parsed_paths = ConfigSectionView( self.tree.root ).evaluate_list( '__inherit__', platform_paths, (self.tree.root,) )

        ### A node may not inherit itself
        if self.filepath in map(Path, parsed_paths):
            raise Config.InheritSelfError( str(self.filepath) )

        ###
        return parsed_paths


    @property
    def parents( self ) :
        ''' the full ordered set of all parent nodes, after recursive linearization'''

        parent_paths    = self.__inherit__
        parents         = list( )
        for parent_path in parent_paths :


            parent      = self.tree.nodes[ Path(parent_path) ]
            parents.append( parent )
            parent_parents = parent.__inherit__

            ### Node A may not inherit Node B, if Node B inherits Node A
            if str(self.filepath) in parent_parents:
                raise Config.InheritLoopError(
                      '\n' + term.dcyan( 'Config:' ) + f' {str(self.filepath)}'
                    + '\n' + term.dcyan( 'Parent:' ) + f' {str(parent.filepath)}'
                    + ''   # raise Config.ParentNotfound
                )

            parents.extend( map(lambda path: self.tree.nodes[Path( path )], parent_parents) )
            # log.info(term.white('parents:', str(self.filename), parent_path ))

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
        ''' unchained and unprocessed '''
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
            # print( term.green('PARSED~~~~~'), parsed_dict )
        except KeyError as e :
            parsed_dict = OrderedDict()

        # print( term.white( '_export' ), parsed_dict )
        return parsed_dict

    @property
    def exports(self) -> OrderedDict:
        ''' a dictionary of exporter names mapped to a list of (output names, list of section keys)'''

        result = OrderedDict()
        result = OrderedDict()
        for node in self.key_resolution_order :
            #print( term.cyan( 'node:' ), node)
            for destination, speclist in node.__export__:
                parsed_destination = ConfigSectionView(self, 'path').evaluate('__destination__', destination)
                assert len(speclist) > 1
                exporter_name   = speclist[0]
                export_subtrees = OrderedSet(speclist[1:])
                # print( term.white( '    export' ), destination, term.white('|'), exporter_name, term.white( '|' ), export_subtrees )

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
    ''' implement the multi chainmap key resolution algorithm on a config and its tree
        each instance of this class keeps track of a level of index depth in the value parsing algorithm
        dynamic chainmap - search config parents for keys if not found in the current one
        token expression substitution - evaluate to values from other keys, sections, and/or files
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
            # print( term.green( 'key:' ), key )
            key_union.add( key )
        return list( key_union )

    def items( self ) :
        '''key-value tuples for the current subtree only, with values resolved'''

        # print( term.blue( 'items' ), self.section_keys )
        yield from map( lambda key : (
                key,
                getdeepitem( self.config, [*self.section_keys, key] )
            ),
            self.keys()
        )

    def values( self ) :
        for value in (p for k, p in self.items()) :
            yield value

    def paths( self ) :
        for path in map( Path, self.values() ) :
            yield path


    ####################
    def allkeys( self ) :
        '''get the union of keys for all nodes in the key resolution order'''

        key_union = GreedyOrderedSet()
        for node in self.config.key_resolution_order :
            # print(term.cyan('node:'), node, self.section_keys, '\n',
            #       getdeepitem( node._yaml_data, self.section_keys ))
            for key in getdeepitem(node._yaml_data, self.section_keys).keys():
                # print(term.green('    key:'), key)
                key_union.add(key)
        #     print( term.green( '\n------------------------------------' ))
        # print(term.cyan( '\n------------------------------------' ))
        return list(key_union)

    def allitems( self ) :
        '''same as items, but uses allkeys method'''

        # print( term.blue( 'allitems' ), self.section_keys )
        yield from map(
            lambda key : (
                key,
                getdeepitem( self.config, [*self.section_keys, key], self.config.key_resolution_order )
            ),
            self.allkeys( )
        )

    def allvalues( self ) :
        ''' full-depth values '''
        yield from (value for key, value in self.allitems())

    def allpaths(self):
        ''' full-depth values, convert values to Path objects before returning them '''
        yield from starmap(lambda k, v: (k, Path(v)), self.allitems())


    ####################
    def setdefault( self, key, default, kro ) :
        ''' support for getdeepitem on Config object'''
        # print( term.blue( "-----------------------------" ), 'begin setdefault', self.config, self.section_keys, term.white( key ) )
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
        # print(term.blue("-----------------------------"), 'begin __getitem__', self.config, term.white(key))
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
            # print(term.red("PRUNE KRO"))
            # listprint(kro)
            # print(term.red('---'), self.config)
            pruned_kro = deque( kro )
            try:
                while pruned_kro.popleft( ) != self.config : pass
            except IndexError:
                pruned_kro = (self.config.tree.root,)
            # listprint(pruned_kro)
            # print( term.red( '--- pruned' ) )


        ### check current node
        # print( term.pink( 'CHECK SELF' ), self.config.filepath, 'keys', self.section_keys, term.white( key ) )
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

                # print( term.cyan('~~~Cache List Result'), self.section_keys, key, self.config , parsed_list)
                getdeepitem( self.config._final_cache, self.section_keys)[key] = parsed_list   # CACHE LIST ###
                return parsed_list

            else :                                                                              # Scalar Value Found
                final_value = self.evaluate( key, raw_value , kro=pruned_kro)

                # print( term.cyan('~~~Cache Scalar Result'), self.section_keys, key, final_value )
                getdeepitem( self.config._final_cache, self.section_keys )[key] = final_value   # CACHE VALUE ###
                return final_value


        ### check parents
        # print(term.pink('CHECK PARENTS'), self.config.filepath, 'keys', self.section_keys, term.white(key))
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
                # print(term.blue('parent_value:'), self.section_keys, key, parent_value, self.config.filepath)
                return parent_value

        # not found
        # print('__getitem__', key, term.red('|'), self.config, term.red( '|' ),self.section_keys)
        raise KeyError(str(key)+' not found.')


    ####################
    def evaluate_list(self, key, raw_list, kro):
        ''' evaluate each element of the list, and return the list of parsed values '''
        parsed_list = []
        # print(term.yellow('------------'), 'EVALUATE LIST', raw_list)
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
        # print(term.green('EVALUATE:'), key, value, self)

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
            print(term.red('SUBSTITUTE'), key, value, self)
            raise e

        except RecursionError as e:
            raise RecursionError( self.config.filepath, self.section_keys, key, value) from None


    # log.debug( "After re.subn:  ", result, " | ", count, "|", expression_replacer.counter[0] )

        total_count += expression_replacer.counter[0] + count# ToDo: Replace monkey patch with class
        # log.debug( "Subn Result: ", result, ' after ',total_count )

        return result, total_count


    ####################
    def expression_parser( self, key, kro=(), listeval=False ) :
        ''' factory that creates a replace function to be used by regex subn
            process ${configpath::section:key} token expressions:
            -    key:        look up value in current section of current config
            -    sections:   [optional] look for key in a different section
            -    configpath: [optional] begin key lookup in a different node

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
            # print("value", term.green(matchobj.group(0)))
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

            # print(term.cyan("subn result:"), result, term.cyan('|'), key, term.cyan( '|' ), matchobj.group(0))
            if isinstance(result, OrderedDict) and len(result) == 0:
                raise Config.SubstitutionKeyNotFoundError(''.join(str(s) for s in [
                    'Could not find ', target_configpath, '::', target_sections,':', target_key,
                    ' for inserting into ', self.config.filepath, '::', self.section_keys,':', key,
                ]))
            elif isinstance(result, list) and matchobj.group(0) == matchobj.string and listeval and token == '@':
                ### WARNING: use a hack to return a list out from the regex substitute
                ### so we can later use it to extend a list we're substituting into
                # log.info(term.blue('*'*30), 'LIST INSERT' )
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

        ### Find Root File
        try:
            root_file = stack_of_files( target_path, '__root__.yml' )[0]
            root_path = root_file.parents[0]
        except IndexError as e:
            raise FileNotFoundError("Could not find '__root__.yml' file in <" +str(target_path)+ ">, or inside any parent directory")

        ### Find Env File
        try :
            env_file = stack_of_files( target_path, '__env__.yml' )[0]
            env_path = env_file.parents[0]
        except IndexError as e :
            log.info( 'Warning - __env__.yml file not found. Using root node...' )
            env_file = None
            env_path = root_file.parents[0]

        print("env_file", env_path)
        self = cls( root_file=root_file, env_path=env_path )

        if env_file is not None:
            self.add_node(env_file)

        # todo: instead of searching for files, load files referenced by root and env, recursively
        # with temporary_working_directory( root_path ) :
        #     for file in find_yamls( root_path ) :
        #         if file != self.root.filepath :
        #             # todo: skip files that throw an invalid config exception
        #             self.add_node( Path( file ) )

        self.finalize()
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
            assert target_file not in self.nodes
            node = Config.from_yaml( target_file, tree=self )
            self.nodes[node.filepath] = node
            return node
        except Config.EmptyFileWarning as e:
            log.debug( 'Config.EmptyFileWarning:', e )
        except Config.ProtocolError as e:
            log.debug( 'Config.ProtocolError:', e )
        except AssertionError as e:
            log.info( f'Node already exists {str(target_file)}' )

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
            if no filepath is given, return the root node
            if only a path is given, try to guess the filename
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

add_pprint( ConfigTree )
add_pprint( Config )


#----------------------------------------------------------------------#
