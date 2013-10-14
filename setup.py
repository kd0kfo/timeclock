#!/usr/bin/env python

from setuptools import setup

the_scripts = ['scripts/punch', 'scripts/unixtime.py']

setup (name ='timeclock',
       version = '1.1.0',
       url = 'http://code.davecoss.com',
       license = 'GPL v3',
       description = 'Time clock program',
       author='David Coss',
       author_email='David.Coss@stjude.org',
       packages = ['timeclock'],
       scripts = the_scripts,
       )

