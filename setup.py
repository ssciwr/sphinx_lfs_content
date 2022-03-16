from setuptools import find_packages, setup
import os


# Read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="sphinx_lfs_content",
    version="1.1.0",
    author="Dominic Kempf",
    author_email="dominic.kempf@iwr.uni-heidelberg.de",
    description="Ensure existence of LFS content in your LFS builds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix ",
        "License :: OSI Approved :: MIT License",
    ],
)
