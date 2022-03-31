# Change Log

## Background

### Versioning

H2O Nitro follows [Semantic Versioning](https://semver.org/). Minor and patch releases should never contain breaking
changes.

When referencing the [`h2o-nitro` package](https://pypi.org/project/h2o-nitro/) from your `requirements.txt`
or `setup.py`, you should always use a version constraint such as `>=4.2, <5` (any version 4.2 or greater, but less than
5), since major releases of H2O Nitro do include breaking changes.

### Support Policy

For LTS releases, bug fixes are provided for 2 years and security fixes are provided for 3 years. These releases provide
the longest window of support and maintenance. For general releases, bug fixes are provided for 6 months and security
fixes are provided for 1 year.

## v0.2.0

Mar 30, 2022

- Added
    - Run `nitro create` to create a new app using Flask, Tornado or Starlette.
    - Run `nitro tour` to launch the built-in interactive tour and documentation.
- Changed
    - `box()` defaults to text blocks instead of textboxes.

## v0.1.0

Mar 29, 2022

- Initial version
