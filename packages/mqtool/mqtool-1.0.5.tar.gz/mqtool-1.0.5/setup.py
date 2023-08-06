#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 BussanQ

import sys
from os.path import dirname, join

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

from setuptools import (
    find_packages,
    setup,
)


requirements = [str(ir.req) for ir in parse_requirements("requirements.txt", session=False)]


setup(
    name='mqtool',
    version='1.0.5',
    description='bq tool',
    packages=find_packages(exclude=[]),
    author='BussanQ',
    license='BussanQ',
    package_data={'': ['*.*']},
    install_requires=requirements,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
    ],
)
