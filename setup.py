#!/usr/bin/env python

from setuptools import setup, Command

class Tester(Command):
    user_options = []

    def initialize_options(self):
        import os
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        import test
        print("Testing date2unix")
        if not test.test_date2unix():
            print("FAILED")
            exit(1)
        else:
            print("Success!")


the_scripts = ['scripts/punch', 'scripts/date2unix']

setup (name ='timeclock',
       version = '1.3.0',
       url = 'http://code.davecoss.com',
       license = 'GPL v3',
       description = 'Time clock program',
       author='David Coss',
       author_email='David.Coss@stjude.org',
       packages = ['timeclock'],
       scripts = the_scripts,
       cmdclass={'test': Tester}
       )

