#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Setup file for Linux distribution of the Data Modelling Toolchain (DMT).

Usage:  python setup.py sdist   --> to create a tarball
        python setup.py install --> to install in python directory
'''

from setuptools import setup, find_packages

setup(
    name='dmt',
    version="2.1.0",
    packages=find_packages(),
    author='Thanassis Tsiodras',
    author_email='Thanassis.Tsiodras@esa.int',
    description='TASTE Data Modelling Technologies based on ASN.1',
    #long_description=open('README.md').read(),
    include_package_data=True,
    url='http://taste.tuxfamily.org',
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5'
    ],
    install_requires=[
        'coverage==3.7.1',
        'flake8==2.6.0',
        'mypy-lang==0.4.2',
        'pyflakes==1.2.3',
        'pylint==1.5.6',
        'pytest==2.6.3',
        'astroid==1.4.6',
        'pycodestyle==2.0.0',
        'typing==3.5.2.2',
    ],
    entry_points={
        'console_scripts': [
            'asn2aadlPlus = dmt.asn2aadlPlus:main',
            'asn2aadlVDM = dmt.asn2aadlVDM:main',
            'asn2dataModel = dmt.asn2dataModel:main',
            'aadl2glueC = dmt.aadl2glueC:main',
            'msgPrinter = dmt.msgPrinter:main',
            'msgPrinterASN1 = dmt.msgPrinterASN1:main',
            'smp2asn = dmt.smp2asn:main',
            'dmt = dmt.commonPy:print_version'
        ]
    }
)
