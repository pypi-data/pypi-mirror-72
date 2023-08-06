#! /usr/bin/env python3

import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(fname):
    return open(os.path.join(here, fname)).read()


with open(os.path.join(here, "yaqd_core", "VERSION")) as version_file:
    version = version_file.read().strip()

extra_files = {"yaqd_core": ["py.typed", "VERSION", "AVRO_VERSION"]}

setup(
    name="yaqd-core",
    packages=find_packages(exclude=("tests", "tests.*")),
    package_data=extra_files,
    python_requires=">=3.7",
    install_requires=["appdirs", "toml", "fastavro"],
    extras_require={
        "docs": ["sphinx", "sphinx-gallery>=0.3.0", "sphinx-rtd-theme"],
        "dev": ["black", "pre-commit", "pydocstyle"],
        "aserial": ["pyserial"],
        "tests": ["pytest", "yaqc>=0.2.0", "numpy"],
    },
    version=version,
    description="Core structures for yaq component daemons",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="yaq Developers",
    author_email="git@ksunden.space",
    license="LGPL v3",
    url="https://yaq.fyi",
    project_urls={
        "Source": "https://gitlab.com/yaq/yaqd-core-python",
        "Documentation": "http://yaqd-core-python.yaq.fyi/",
        "Issue Tracker": "https://gitlab.com/yaq/yaqd-core-python/issues",
    },
    keywords="spectroscopy science multidimensional hardware",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    zip_safe=False,
)
