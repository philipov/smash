# smash alpha 0.0.4
a modular non-interactive shell that's better for the environment

--------------------------------------------------------------------------

### Table of Contents:

- [Motivation and Objectives](#motivation-and-objectives)
- [Components](#components)
- [Ideology](docs/manifesto.md)
    - Reproducible Research
    - Modularity
    - Test-driven
    - A Command-Line IDE
    - Scripting in python
    - [Packaging Methodology](docs/manifesto.md#packaging-methodology)
- [Tutorials](docs/howto.md)
    - [Installation](docs/howto.md#installation)
    - [Getting Started](docs/howto.md#getting-started)
    - [Modular Configuration System](docs/howto.md#modular-configuration-system)
- [API Reference](docs/api.md)
    - nope


--------------------------------------------------------------------------
### Motivation and Objectives
- smash's yamlisp configuration is not an abstraction layer, it is a tool for factorization
- need to avoid all-or-nothing adoption patterns
    - take a small thing you already do and insert smash into it.
    - run smash's config side-by-side with the existing implementation and compare results
- I want a single source of truth for values in my shell environment variables and various configuration files, and for use inside other python programs.
- yaml is easier to read than xml or json. python is even better, but less secure (does it have to be?)
    - but it doesn't have a great syntax for constructing values out of tokens, like shell scripts can.
- it would be great to convert all my other configuration into a single yml file per project.
    - but I also want to split it up into configuration modules for each separate concern.  
- conda has environment.yml, but also requires a shell script to set environment variablse. What's up with that?
- pipenv doesn't seem to even care about environment variables.
- Ansible is for building immutable servers, not for living research and development environments.
    - environments aren't immutable, and changes to their state need to be version controlled.
- On the other hand, the same process used during R&D should be easy to promote to production, and also easy to load into a support environment.
    - It needs to be easy to adopt gruadually without demanding total devotion to a walled garden.
    - It needs to work on windows, mac, and linux, on my laptop, without destroying everything else.
    - the package/environment manager should also manage the git project, not merely support installing from one.
    - the environment manager should integrate a solution for secrets management across different hosts  
- possible to construct either deployment archives or docker images
    - bring-your-own-python, or pyinstaller bootloader? some combination of both...
- control a remote environment over ssh 
    - integration to task scheduling through dask
- use the same single source of truth for configuring both scheduled jobs and services
    - integration to some sort of service registry
- allow interoperability with language-specific package managers
    - track dependencies for libraries from multiple languages in one environment

---
### Components:

- `smash`
    - `smash.core`  - main library provides abstraction classes and a plugin system
    - `smash.tool`  - transactional model for manipulating environment state
    - `smash.bang`  - `smash!` manage instances and boxes
    - `smash.box`   - put your research into [boxes](https://www.youtube.com/watch?v=XUwUp-D_VV0) and it'll all come out the same
    - `smash.dash`  - `smash-` graphical user interface; visualize interconnected instances
    - `smash.test`  - wrapper for running development, qa, deployment, and validation tests
    - `smash.setup` - smash package metadata used by setup.py. includes variations for testing and development.


- `powertools`  - basic utilities library
- `yamlisp`     - YAML-based scripting/configuration language
- `cogwright`   - wheel construction utility







--------------------------------------------------------------------------
