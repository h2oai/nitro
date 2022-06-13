#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup


def get_version(package):
    path = os.path.join(package, "version.py")
    init_py = open(path, "r", encoding="utf8").read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_long_description():
    return open("README.md", "r", encoding="utf8").read()


def get_packages(package):
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name="h2o_nitro",
    version=get_version("h2o_nitro"),
    url="https://nitro.h2o.ai/",
    description="The simplest way to build web apps. No front-end experience required.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Prithvi Prabhu",
    author_email="prithvi.prabhu@gmail.com",
    packages=get_packages("h2o_nitro"),
    python_requires=">=3.7",
    install_requires=[
        "click",
        "msgpack>=1.0",
    ],
    include_package_data=True,
    license_files=('LICENSE',),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 2 - Pre-Alpha',
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Communications :: Chat',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Widget Sets',
        'Topic :: System :: Distributed Computing',
    ],
    project_urls={
        "Documentation": "https://nitro.h2o.ai/",
        "Source": "https://github.com/h2oai/nitro",
        "Issues": "https://github.com/h2oai/nitro/issues",
        "Changelog": "https://nitro.h2o.ai/change-log/",
    },
)
