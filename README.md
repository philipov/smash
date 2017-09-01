# smash
modular reproducible research environment manager

--------------------------------------------------------------------------

### Table of Contents:

- Purpose
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

- `cogwright`
- `powertools`

- `smash`
    - `smash.sys`
    - `smash.env`
    - `smash.git`
    - `smash.dash`
    - `smash.boot`
    - `smash.tools`


--------------------------------------------------------------------------

### Purpose

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


---
### Modular Configuration System 

##### class-like configuration by way of a modified chainmap on top of yaml source

##### `${configname@section:key}` token expressions

##### `__root__.yml` defines the top of the filesystem

##### `__env__.yml` configures the point-of-view and entry for execution environments

##### `__pkg__.yml` specifies the contents of a reusable configuration package

##### task description files
 
##### plugins

##### compiling configurations with `Exporter`

- `ExportEnvironment`
- `ExportDebug`

##### binding contextual operations to file types using `FileHandler`

- `YAMLHandler`

##### wrapping subprocess utilities inside `Tool`

- `Task`
- `Loader`
- `Validator`
- `Daemon`
- `Monitor`


##### creating new system layouts using `RootTemplate`

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
