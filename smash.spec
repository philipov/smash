# -*- mode: python -*-

block_cipher = None

#----------------------------------------------------------------------#

from pathlib import Path
import os

root_path = Path( os.getcwd() )

# a = Analysis( ['smash.py'],
#               pathex=[str( root_path )],
#               binaries=[],
#               datas=[],
#               hiddenimports=[],
#               hookspath=[],
#               runtime_hooks=[],
#               excludes=[],
#               cipher=block_cipher,
#               win_no_prefer_redirects=False,
#               win_private_assemblies=False,
#               )

def Entrypoint( dist, group, name,
                scripts=None, pathex=None, hiddenimports=None,
                hookspath=None, excludes=None, runtime_hooks=None ) :
    import pkg_resources

    # get toplevel packages of distribution from metadata
    def get_toplevel( dist ) :
        distribution = pkg_resources.get_distribution( dist )
        if distribution.has_metadata( 'top_level.txt' ) :
            return list( distribution.get_metadata( 'top_level.txt' ).split() )
        else :
            return []

    hiddenimports = hiddenimports or []
    packages = []
    for distribution in hiddenimports :
        packages += get_toplevel( distribution )

    scripts = scripts or []
    pathex = pathex or []
    # get the entry point
    ep = pkg_resources.get_entry_info( dist, group, name )
    # insert path of the egg at the verify front of the search path
    pathex = [ep.dist.location] + pathex
    # script name must not be a valid module name to avoid name clashes on import
    script_path = os.path.join( workpath, name + '-script.py' )
    print("creating script for entry point", dist, group, name )
    with open( script_path, 'w' ) as fh :
        print( "import", ep.module_name, file=fh )
        print( "%s.%s()" % (ep.module_name, '.'.join( ep.attrs )), file=fh )
        for package in packages :
            print( "import", package, file=fh )

    return Analysis( [script_path] + scripts, pathex, hiddenimports, hookspath, excludes, runtime_hooks )


a = Entrypoint( 'smash', 'console_scripts', 'smash' )

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='smash',
    debug=False,
    strip=False,
    upx=True,
    console=True
)

def collect_data( subpath ) :
    global a

    for path, _, _ in os.walk( str( root_path / subpath ) ) :
        rel_path = Path( path ).relative_to( root_path )
        a.datas += Tree( path, prefix=rel_path )

# collect_data( 'pkgs' )
# collect_data( 'envs' )
# collect_data( 'repo' )
# collect_data( 'sys' )

#----------------------------------------------------------------------#

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,

    strip=False,
    upx=True,
    name='smash'
)


#----------------------------------------------------------------------#
