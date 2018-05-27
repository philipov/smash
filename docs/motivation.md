### a mess of configuration files and system state

#### configuration is code
- factor code to separate concerns
- combine code to avoid repeating yourself
- need to avoid platform-specific shell scripts for compatability reasons
- need to avoid generic programming languages for security reasons
- need to be able to refer to previous config values to construct new values

#### use cases
- need to handle non-onetick dependencies
- individual researchers develop new prototype: how does it get distributed?
- need to coordinate development with a client site
  - full on-premises
  - on-premises deployment with remote support
  - hybrid solution with split deployment
  - full hosted
- version control
  - avoid duplicating the same dependency for each project
  - submodules and subtree merges are too inconvenient
  - can't use monorepo because of on-prem deployments

#### serialization formats
- xml and json are bulky and hard to read
- yaml is good, but lacks the ability to construct nev values using old values
  - introduce a token substitution syntax: `${configfile::section:section:key}`
  - class-like inheritance between config files
 
 
#### next steps
- refactor parsing algorithm
- package bestex solution using smash
- automated installation integrations
  - conda for package management
  - ansible? for cluster provisioning
  - vault for secrets management
  - consul for service discovery
- debug features: 
  - parse tree tracing
  - reverse lookup a key for a value
