#!/usr/bin/python

from distutils.core import setup

import sysmon

setup(name='YASMon',
      version=sysmon.version(),
      description='yet another system monitor',
      author='Scott Lawrence',
      author_email='bytbox@gmail.com',
      maintainer='Scott Lawrence',
      maintainer_email='bytbox@gmail.com',
      url='http://github.com/bytbox/yasmon',
      requires=['PyQt4'],
      packages=['sysmon'],
      scripts=['yasmon'],
      data_files=[('/usr/share/man/man1',['yasmon.1','yasmond.1'])]
      )
