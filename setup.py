#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
from distutils.core import setup

setup(name='TCFlib',
      version='0.2.6',
      description='Python TCF library',
      author='Frederik Elwert',
      author_email='frederik.elwert@web.de',
      url='https://github.com/SeNeReKo/TCFlib',
      packages=['tcflib', 'tcflib.tagsets'],
      package_data={'tcflib.tagsets': ['data/dc-1345.dcif']},
     )
