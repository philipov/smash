
---
### Installation
- `pip install smash`
- `smash install <install_path>`
- `smash setup_windows` _(optional)_

##### installing a smash payload

##### building a smash payload


---
### Getting Started

##### dynamic virtual environments
- `smash root <template>`
- `smash env create`

##### git-based centralized config

##### installing a package
- `smash pkg <pkgname>`

##### running tests
- `smash test <target>`
- `./sh/win/tests.bat`
- `./sh/nix/tests.sh`

##### running a command
- `smash cmd ...`

##### contextual file operations
- `smash run <filepath>`
- windows context menu options

##### daemon-mode
- `smash start <filepath>`
- service registration
- refreshing the configuration

##### packaging, environment management, conda, and cookiecutter

##### jupyter notebooks

##### scheduling and deployment

##### docker-compose and helm

##### backups

##### email notifications

##### customizing the terminal console and shell


---
### Modular Configuration System

##### class-like configuration by way of a modified chainmap on top of yaml source

##### `${configname@section:key}` token expressions

##### `__root__.yml` defines the top of the filesystem

##### `__env__.yml` configures the point-of-view and entry for execution environments

##### `__pkg__.yml` specifies the contents of a reusable configuration package

##### task description files

##### compiling configurations with `Exporter`

- `ExportEnvironment`
- `ExportDebug`
- `ExportYAML`
- `ExportXML`
- `ExportINI`

##### binding contextual operations to file types using `FileHandler`

- `YAMLHandler`
- `EXEHandler`
- `ScriptHandler`

##### wrapping subprocess utilities inside `Tool`

- `Task`
- `Loader`
- `Validator`
- `Daemon`
- `Monitor`
- `Service`


##### creating new system layouts using `RootTemplate`

##### creating project-specific extensions using the plugin system

##### specifying configurations directly using python classes
