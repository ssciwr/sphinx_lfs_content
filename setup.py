from setuptools import find_packages, setup

setup(
    name="sphinx_lfs_content",
    version="0.1.0",
    author="Dominic Kempf",
    author_email="dominic.kempf@iwr.uni-heidelberg.de",
    description="Ensure existence of LFS content in your LFS builds",
    long_description="",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Linux ",
        "License :: OSI Approved :: MIT License",
    ],
)
