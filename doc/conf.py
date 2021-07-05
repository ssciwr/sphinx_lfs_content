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

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = []

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Make sure that classes are documented by their init method
autoclass_content = "init"

if os.environ.get("READTHEDOCS", "False") == "True":

    # By default, Read the Docs does not recognize git lfs content
    # This workaround to install and execute git-lfs on Read the Docs
    # is taken from https://github.com/readthedocs/readthedocs.org/issues/1846

    def syscall(cmd):
        env=os.environ
        env["PATH"] = os.environ["PATH"] + os.path.pathsep + os.getcwd()
        env["GIT_DIR"] = os.path.join(os.getcwd(), "..", ".git")
        env["GIT_WORK_TREE"] = os.path.join(os.getcwd(), "..", ".git")
        subprocess.check_call(cmd.split(), env=env)

    print(f"GIT_DIR: {os.environ.get('GIT_DIR', 'NOTSET')}")
    print(f"Toplevel git dir without modifying GIT_DIR: {subprocess.run('git rev-parse --show-toplevel'.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')}")

    print("Toplevel git dir with modifying GIT_DIR")
    syscall("git rev-parse --show-toplevel")
    syscall("wget https://github.com/git-lfs/git-lfs/releases/download/v2.7.1/git-lfs-linux-amd64-v2.7.1.tar.gz")
    syscall("tar xvfz git-lfs-linux-amd64-v2.7.1.tar.gz")
    syscall("git-lfs install")
    syscall("git-lfs fetch")
    syscall("git-lfs checkout")

    print(f"Working dir: {os.getcwd()}")
    print(subprocess.run(['ls', '--full'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
