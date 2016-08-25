#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of robotframework-dnslibrary.
# https://github.com/someuser/somepackage

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, lucamaro <luca.maragnani@gmail.com>

from setuptools import setup, find_packages
from DNSLibrary import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='robotframework-dnslibrary',
    version=__version__,
    description='Robotframework library to test DNS service',
    long_description='''
Robotframework library to test DNS service
''',
    keywords='',
    author='lucamaro',
    author_email='luca.maragnani@gmail.com',
    url='https://github.com/someuser/somepackage',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'robotframework-dnslibrary=robotframework_dnslibrary.cli:main',
        ],
    },
)
