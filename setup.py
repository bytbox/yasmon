#!/usr/bin/python

from distutils.core import setup

import sysmon

setup(name='modred',
      version=sysmon.version(),
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
