#!/usr/bin/env python

from distutils.core import setup

setup(name='topo',
      version='0.1',
      description='IP topography visualization',
      author='Greg Toombs',
      url='https://github.com/reinderien',
      requires=['netifaces',
                'netaddr'
                ])
