#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import re


def get_version(version_file):
    pattern = r"^__version__ = ['\"]([^'\"]*)['\"]"
    match = re.search(pattern, open(version_file, "rt").read(), re.MULTILINE)
    if match:
        return match.group(1)

    raise RuntimeError("Unable to find version string in %s." % (version_file,))


with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = ["wheel", "pytz"]

test_requirements = ["pytest>=3"]

setup(
    name="hi-dateinfer",
    author="Jeffrey Starr",
    author_email="will@pedalwrencher.com",
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="""Infers date format from examples, by using a series of pattern matching and rewriting rules to compute a 'best guess' datetime.strptime format string give a list of example date strings.""",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    license="Apache Software License 2.0",
    include_package_data=True,
    keywords="dateinfer",
    packages=find_packages(include=["hidateinfer", "hidateinfer.*"]),
    setup_requires=[],
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/hi-primus/hi-dateinfer",
    version=get_version("hidateinfer/__init__.py"),
    zip_safe=False,
)
