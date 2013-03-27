#!/usr/bin/env python

from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

setup(
    name = 'bottle_cql',
    version = '0.1',
    description = 'Pycassa integration for Bottle.',
    author = 'David McNelis',
    author_email = 'dmcnelis@emergingthreats.net',
    url = 'http://www.github.com/dmcnelis/bottle-pycassa',
    license = 'MIT',
    platforms = 'any',
    py_modules = [
        'bottle_cql'
    ],
    requires = [
        'bottle (>=0.9)',
        'cql (>=1.4.0)'
    ],
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    cmdclass = {'build_py': build_py}
)
