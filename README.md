# sphinx_lfs_content

[![PyPI version](https://badge.fury.io/py/sphinx-lfs-content.svg)](https://badge.fury.io/py/sphinx-lfs-content)
[![Documentation Status](https://readthedocs.org/projects/sphinx-lfs-content/badge/?version=latest)](https://sphinx-lfs-content.readthedocs.io/en/latest/?badge=latest)

Git LFS is a popular method to store large files like e.g. documentation assets in git repositories.
Building such documentation on a system without Git LFS will typically result in broken documentation. 
`sphinx_lfs_content` is a minimalistic Sphinx extension that ensures that `git-lfs` is installed and otherwise installs it and fetches LFS content.
It is motivated by the [lack of LFS support on readthedocs.org](https://github.com/readthedocs/readthedocs.org/issues/1846).

## Installation

The extension can be installed from PyPI using `pip`:

```python
python -m pip install sphinx_lfs_content
```

If you use a requirements file to describe the dependencies of your documentation build, simply add `sphinx_lfs_content` to it.

## How to use it

Add the following lines to your `conf.py`:

```python
# The list of enabled extensions
extensions = [
    "sphinx_lfs_content",
]
```

That's all. The extension will check whether the system has `git-lfs` and download a version
from the [`git-lfs` GitHub page](https://github.com/git-lfs/git-lfs), verify its checksum
and checkout any LFS content.

Additionally, a configuration value `lfs_content_post_commands` is available. It accepts a list
of strings with commands that will be executed after the git-lfs checkout was performed.
This can be used to resolve chicken-egg situations with other setup code.

## Restrictions

The extension is very likely to only work on Linux right now, as it does not properly select the `git-lfs` archive to download.
