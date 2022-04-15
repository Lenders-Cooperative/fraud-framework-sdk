===================
Contributor's Guide
===================


New Features, Bug Reports & Fixes
=================================
If you discover any bugs or critical issues, please create a GitHub issue here and we will address it as soon as possible.
All fixes are greatly appreciated. 

For all new features, please submit a PR and we will review it at our earliest availability.
If you'd like any new features to be added to this project, describe the problem you want to solve in a new GitHub issue.


Tests, Docs, etc.
===========================
Any updates, enhancements, or additions to our testing suite or documentation are greatly appreciated!


Local Development
=================

Setup
~~~~~
1. Install Poetry
    - See https://python-poetry.org/docs/ for further information
    - We highly recommend using the cURL method for installation
    - Note: for Windows users, there are some known issues using GitBash with poetry - we recommend using Powershell/cmd if available.
2. `poetry install`

Testing
~~~~~~~
1. `poetry run pytest`
    - Run tests with current Python interpreter
2. `poetry run tox`
    - Run tests with all supported Python interpreters (if present)

Linting, Typing & Code Style
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. `poetry run black fraud_framework_sdk`
    - Format using Black formatter with project's `pyproject.toml` settings
2. `poetry run isort fraud_framework_sdk`
    - Format using `isort` with project's `pyproject.toml` settings
3. `poetry run mypy fraud_framework_sdk`
    - Run type checking


Distribution (Internal)
=======================

1. Update version numbers in `pyproject.toml` and `__init__.py` file within `fraud_framework_sdk/`
2. `poetry build`
    - Build distribution files: `sdist`, `.tar.gz`, `.whl`, etc.
3. `poetry publish`
    - Deploy final package on PyPi
