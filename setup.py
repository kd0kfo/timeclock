#!/usr/bin/env python

from setuptools import setup, Command


class Tester(Command):
    user_options = []

    def initialize_options(self):
        import test
        import os
        import os.path as OP
        self._dir = os.getcwd()

        if OP.isfile(test.TEST_CLOCK_FILE):
            os.remove(test.TEST_CLOCK_FILE)

    def finalize_options(self):
        pass

    def run(self):
        import test
        from time import sleep

        test.date2unix()
        test.punchin()
        print("Sleeping 2 seconds")
        sleep(2)
        test.switch_punch()
        print("Sleeping 2 more seconds")
        sleep(2)
        test.punchout()
        test.summary()


the_scripts = ['scripts/punch', 'scripts/date2unix']

setup (name ='timeclock',
       version = '1.5.1',
       url = 'http://code.davecoss.com',
       license = 'GPL v3',
       description = 'Time clock program',
       author='David Coss',
       author_email='David.Coss@stjude.org',
       packages = ['timeclock'],
       scripts = the_scripts,
       cmdclass={'test': Tester}
       )

