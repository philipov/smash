# smash [under construction]
modular reproducible research environment manager

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

- conda has environment.yml, but also requires a shell script to set environment varibalse. What's up with that?

- pip virtual 

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







--------------------------------------------------------------------------
