#!/usr/bin/python

from distutils.core import setup

from sysmon import version

setup(name='modred',
      version=version,
      description='yet another system monitor',
      author='Scott Lawrence',
      author_email='bytbox@gmail.com',
      maintainer='Scott Lawrence',
      maintainer_email='bytbox@gmail.com',
      url='http://github.com/bytbox/yasm',
      requires=['PyQt4'],
      packages=['sysmon'],
      scripts=['yasm'],
      )
