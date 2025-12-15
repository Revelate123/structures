<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/_static/logo-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/_static/logo-light.png">
  <img alt="toms-structures logo" src="docs/_static/logo-light.png">
</picture>
<div align="left">

[![PyPI](https://img.shields.io/pypi/v/toms-structures.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/toms-structures.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/toms-structures)][python version]
[![License](https://img.shields.io/pypi/l/toms-structures)][license]
[![Read the documentation at https://toms-structures.readthedocs.io/](https://img.shields.io/readthedocs/toms-structures/stable.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/Revelate123/structures/actions/workflows/main.yml/badge.svg?branch=main)][tests]

[pypi_]: https://pypi.org/project/toms-structures/
[status]: https://pypi.org/project/toms-structures/
[python version]: https://pypi.org/project/toms-structures
[read the docs]: https://toms-structures.readthedocs.io/
[pre-commit]: https://github.com/pre-commit/pre-commit
[tests]: https://github.com/Revelate123/structures/actions/workflows/main.yml
[license]: https://github.com/Revelate123/structures/blob/main/LICENSE

<img alt="GitHub release (latest by date including pre-releases" src="https://img.shields.io/github/v/release/Revelate123/structures?include_prereleases">

<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/Revelate123/structures?style=flat">

</div>


An unofficial python library companion to AS 3700:2018 Masonry Structures.

## Installation
You can install `toms-structures` via [pip] from [PyPI]:

```shell
pip install toms-structures
```

## Documentation
Documentation for `toms-structures` is currently under construction. The documentation can be found at [https://toms-structures.readthedocs.io/](https://toms-structures.readthedocs.io/).

## Features
- Compression and bending capacity of unreinforced clay / concrete masonry
- Bending capacity of RC blocks

### Why does this project exist?
Many structural engineers in Australia rely on a combination of industry software / excel spreadsheets / hand calculations. It is common for an excel spreadsheet to be passed around with variable amounts of documentation, little or no testing, and no verification that the spreadsheet was not broken at some point in the past. Efforts to fix these issues exist and there certainly are quality excel spreadsheets, but it is generally difficult to achieve and requires outsized organisational efforts to maintain. This project aims to replace some of those excel spreadsheets. 

### Project goals:
1. Provide extensive testing so that outputs are reliable. 
2. Provide thorough documentation so that structural engineers without extensive software engineering training can clearly understand how calculations are performed, what the intended use cases are, what the limitations of the project are, and how they can raise issues/contribute.


## Contributing



## Support

Issue Tracker: https://github.com/Revelate123/structures/issues

## Disclaimer

This library is intended for use by qualified structural engineers. It is the user's responsibility to confirm and accept the output.


[pypi]: https://pypi.org/
[pip]: https://pip.pypa.io/