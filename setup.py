#!/usr/bin/env python

from distutils.core import setup

setup(name='ldaf',
      version='0.5',
      description='Large Data Analysis Framework',
      author='Tobias Specht',
      author_email='specht.tobias@gmx.de',
      url='https://github.com/peckto/ldaf',
      install_requires=open('requirements.txt').readlines()
    )
