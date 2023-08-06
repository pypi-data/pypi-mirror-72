#!/usr/bin/env python
# coding: utf-8
"""
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

"""


"""
Python Dubbo Library Client Server - Setup
 
Created
    2015-4-10 by Joe - https://github.com/JoeCao
"""


import os

from setuptools import setup, find_packages

THISDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(THISDIR)

VERSION = open("version.txt").readline().strip()
HOMEPAGE = "https://github.com/nickfan/dubbo-python3"
DOWNLOAD_BASEURL = "https://github.com/nickfan/dubbo-python3/raw/master/dist/"
DOWNLOAD_URL = DOWNLOAD_BASEURL + "dubbo-python3-%s-py3.6.egg" % VERSION

setup(
    name="dubbo-python3",
    version=VERSION,
    description=(
        "Python3 Dubbo Client"
    ),
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    keywords=(
        "Dubbo, JSON-RPC, JSON, RPC, Client,"
        "HTTP-Client, Remote Procedure Call, JavaScript Object Notation, "
    ),
    author="Nick Fan",
    author_email="nickfan@gmail.com",
    url=HOMEPAGE,
    download_url=DOWNLOAD_URL,
    packages=find_packages(),
    classifiers=[
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications",
        "Topic :: System :: Networking",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    install_requires=["kazoo>=2.0.0", "jsonrpcclient>=3.3.0"],
)
