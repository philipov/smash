# smash [under construction]
modular reproducible research environment manager

--------------------------------------------------------------------------

### Table of Contents:

- Motivation and Objectives
- Components
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
 

--------------------------------------------------------------------------
### Motivation and Objectives

##### configuration is code

- databases constrain how configuration must be supplied 
- clients know what data they want to use. 
- libraries know how they can accept data.
- hosts knows what data is actually available, and where to find it.
- to construct my environment, I need to combine all these separate concerns
- I need to validate environment state as a dependency of my packages
- a user and a server both inherit common information about the functionality of a package, but their relationship to the resources is different.


##### data is code
- the same data set might get processed over and over again with different iterations of my analysis.
    - which version of the data am I looking at? 


##### pip and conda don't seem to offer support for packaged environment variables

- conda requires environments to be set up with shell scripts. 
    - managing shell scriptss for multiple platforms means repeating yourself
- need a configuration build tool suitable for both research/development and deploying to production


##### better version control integration with the package manager

- use repository working copies as development virtual environments within the package management system
- a shell with transactional environment state manipulation
    - version control changes to the environment as they're made
    - interactive and non-interactive modes
- support either monorepo or repository per package 
- a natural end-user workflow for capturing and sharing experimental results, leading to productionization


##### activating environments is lame

- being in the subtree should imply using that environment.
- map environments to subtrees of the filesystem
    - implicitly determine the environment based on the working directory


---
### Components:

- `smash`
    - `smash.core`  - main library provides abstraction classes and a plugin system
    - `smash.tools` - transactional model for manipulating environment state
    - `smash.boot`  - build and deploy new instances
    - `smash.env`   - manage existing environments and create new virtual environments
    - `smash.pkg`   - locate and install packages for use by virtual environments
    - `smash.dash`  - graphical user interface; visualize interconnected instances 
    - `smash.test`  - wrapper for running development, qa, deployment, and validation tests 
    - `smash.setup` - smash package metadata used by setup.py. includes variations for testing and development.


- `powertools` - basic utilities library
- `cogwright` - wheel construction utility


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




--------------------------------------------------------------------------
