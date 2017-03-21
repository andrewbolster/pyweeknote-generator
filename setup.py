#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 bolster <bolster@milo>
#
# Distributed under terms of the MIT license.

"""
Pythonic ish Version of the DoES Liverpool-based Weeknotes generator (for Farset Labs)
"""

from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(name='pyweeknote-generator',
      version='0.1',
      description='Pythonic ish Version of the DoES Liverpool-based Weeknotes generator (for Farset Labs)',
      url='http://github.com/andrewbolster/pyweeknote-generator',
      author='Andrew Bolster',
      author_email='bolster@farsetlabs.org.uk',
      license='MIT',
      packages=['pyweeknote_generator'],
      install_requires=reqs,
      zip_safe=False,
      entry_points={
          'console_scripts':
              ['pyweeknotes=pyweeknote_generator:main']
      }
      )
