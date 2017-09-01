# smash
modular reproducible research environment manager

--------------------------------------------------------------------------

### Table of Contents:

- Installation
- Getting Started
- Modular Configuration System
- Packaging Methodology
- Ideology
    - Reproducible Research
    - Modularity
    - Test-driven
    - A Command-Line IDE
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

---
### Installation
- `pip install smash`
- `smash install <install_path>`
- `smash setup_windows`

##### installing a smash payload

##### building a smash payload


---
### Getting Started

##### dynamic virtual environments
- `smash root <template>`
- `smash env create`

##### running a command
- `smash cmd ...`

##### contextual file operations
- `smash run <filepath>`
- windows context menu options

##### daemon-mode
- `smash start <filepath>`
- refreshing the configuration

##### git-based centralized config

##### running tests

##### packaging, environment management, and conda

##### jupyter notebooks

##### scheduling and deployment

##### backups


---
### Modular Configuration System 

##### class-based configuration by way of a modified chainmap on top of yaml source

##### `${configname@section:key}` token expressions

##### `__root__.yml`

##### `__env__.yml`

##### `__pkg__.yml` 

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
