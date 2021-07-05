# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import subprocess
import sys

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "sphinx_lfs_content"
copyright = "2021, Scientific Software Center, Heidelberg University"
author = "Dominic Kempf"

# The full version, including alpha/beta/rc tags
release = "0.0.1"

# -- General configuration ---------------------------------------------------

# Enabled Sphinx extensions
extensions = [
    "m2r2",
    "sphinx_lfs_content",
]

# The only config value specific to sphinx_lfs_content
# This is the relative path from the location of conf.py to the git
# repository root.
lfs_content_path_to_git_root = ".."
lfs_content_post_commands = [
    "test $(wc -c test.png | awk '{print $1}') -eq 78713"
]
