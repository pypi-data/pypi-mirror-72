python-compare-ast
==================

Compares ASTs of Python files that have been changed in git.

Useful for checking if formatting changes do not modify the behaviour of the source code.


Requirements
------------

Python 3.6 or newer.


Installation
------------

::

    $ pip install python-compare-ast


Usage
-----

::

    $ python-compare-ast [--git-dir <path_to_git_working_dir>]

``git-dir`` defaults to the current directory.

Example output:

::

    $ git clone https://github.com/pallets/click.git
    $ python-compare-ast --git-dir click
    Analysing /absolute/path/to/click/.git
    Repo is clean, comparing changes in latest commit (dfb842d95a7c146d8fe8140c8100065410d95c4d).
    warning: AST does not match for src/click/core.py
    warning: AST does not match for tests/test_options.py
    Found 2 AST differences.

If the git working directory is clean, the files changed in latest commit will be analysed.
If the git working directory is dirty, the dirty files will will analysed.
If no changed files has a different AST then before, ``python-compare-ast`` will exit with status code 0.
However, if there are changes to the AST the exit code will be 1.
