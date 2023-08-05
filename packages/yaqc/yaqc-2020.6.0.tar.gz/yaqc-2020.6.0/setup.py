#! /usr/bin/env python3

import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, "yaqc", "VERSION")) as version_file:
    version = version_file.read().strip()


with open("README.md") as readme_file:
    readme = readme_file.read()


extra_files = {"yaqc": ["VERSION"]}

setup(
    name="yaqc",
    packages=find_packages(exclude=("tests", "tests.*")),
    package_data=extra_files,
    python_requires=">=3.6",
    install_requires=["fastavro"],
    extras_require={"dev": ["black", "pre-commit", "pydocstyle"]},
    version=version,
    description="generic yaq client",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="yaq Developers",
    license="LGPL v3",
    url="https://yaq.fyi",
    project_urls={
        "Source": "https://gitlab.com/yaq/yaqc-python",
        "Documentation": "https://yaq.fyi",
        "Issue Tracker": "https://gitlab.com/yaq/yaqc-python/issues",
    },
    keywords="spectroscopy science multidimensional hardware",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
)
