# b2c-tms-wrapper

`b2c-tms-wrapper` is a user friendly interface to access Shuttl's b2c-tms backend service's functionalities

<!-- Use markdown-toc to build the following section -->

<!-- toc -->

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Running Tests](#running-tests)
- [Releasing](#releasing)

<!-- tocstop -->

## Installation

`pip install b2c-tms-wrapper`

## Basic Usage

Import the b2c-tms-wrapper module:

```python
b2c_tms = B2CTMS(
    b2c_tms_url=Config.B2C_TMS_URL
)

trip: Trip = b2c_tms.get_trip(trip_id)
```
## Running Tests

- pip install ".[test]"
- pytest


## Releasing
- `make bump_version`
- Update [the Changelog](https://github.com/Shuttl-Tech/b2c-tms-wrapper/blob/master/Changelog.md)
- Commit changes to `Changelog`, `setup.py` and `setup.cfg`.
- `make push_tag` (this'll push a tag that will trigger python package checks)
- `make release` (this will release the tag)