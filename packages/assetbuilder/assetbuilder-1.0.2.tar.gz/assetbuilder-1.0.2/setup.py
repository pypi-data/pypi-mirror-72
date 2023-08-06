#!/usr/bin/env python
#
# Copyright 2017 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
from setuptools import setup

setup(
    name="assetbuilder",
    version="1.0.2",
    description="Build & serve your web project's asset files (JS, CSS etc)",
    py_modules=["assetbuilder"],
    author="Oliver Cope",
    license="Apache",
    author_email="oliver@redgecko.org",
    url="https://ollycope.com/software/assetbuilder/latest/",
    bugtrack_url="https://bitbucket.org/ollyc/assetbuilder/issues",
    packages=[],
    keywords=[
        "web",
        "css",
        "minify",
        "javascript",
        "compress",
        "assets",
        "wsgi",
        "bundle",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
    ],
    install_requires=["pathlib", "portalocker", "itsdangerous"],
)
