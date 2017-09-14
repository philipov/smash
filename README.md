# smash
modular reproducible research environment manager

--------------------------------------------------------------------------

### Table of Contents:

- Objectives
- Installation
- Getting Started
- Modular Configuration System
- Packaging Methodology
- Ideology
    - Reproducible Research
    - Modularity
    - Test-driven
    - A Command-Line IDE
    - Scripting in python 
- Tutorials
    - none
- Documentation
    - nope
 
---
##### Components:

- `smash`
    - `smash.core`
    - `smash.boot`
    - `smash.env`
    - `smash.pkg`
    - `smash.dash`
    - `smash.tools`


- `powertools`
- `cogwright`


--------------------------------------------------------------------------

### Objectives
- a just-in-time build system for configuration files and virtual environments
- map environments to subtrees of the filesystem
    - implicitly determine the environment based on the working directory
- use repository working copies as development virtual environments within the package management system
- a shell with transactional environment state manipulation
    - version control changes to the environment as they're made
    - interactive and non-interactive modes
- support either monorepo or multirepo methodologies 
- a natural end-user workflow for capturing and sharing experimental results, leading to productionization


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


---
### Packaging Methodology

##### module types:
- app
- client
- host
- net
- lib
- data

##### factor out the difference between the user and the server

##### separate the general solution and the client's application

##### separate the resources on a host from the resources on a network/cluster

##### data specifications vs state

##### version controlling data


--------------------------------------------------------------------------
