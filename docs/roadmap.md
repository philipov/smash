---

- Installation package for windows and linux
    - PyInstaller?
    - Miniconda

- hierarchical configuration compilation
    - construct Config and ConfigTree by converting yaml_data directly
        to classes and rely on python's class inheritance
    - exports could be defined in the config files; this requires linking with plugins

- plugins to define tools, config subclasses, output writers
    - testing module for plugins to use

- reorient the config system in terms of the output files to be generated

- download resources from git or ftp to create a distribution archive
- config validation using unit testing techniques


- interface with version control as a package repository
    - support repository-per-package and monorepo

- use smash to write tho config files for a new conda env

- support specifying configuration for docker containers
    - Helm?

- use jupyter as an interface for the smash environment

- when pytest blows up horribly, find a way to get into interactive mode to check the error

---

- How does AWS fit in? This should work on a local client desktop, a on-prem server farm, or a cloud cluster
- Leave scheduling to other systems; goal is to plug into whatever someone is using.

---

- draw an inheritance graph for an environment
    - use the config system to draw a network diagram
- report config values in parsed format, 
    - and as the tree of raw values used to compose the result

- reverse lookup: for a given value, find a key  

---

- support multiple package managers in dependencies
    - viper
    - pip
    - conda
    - cargo

---
