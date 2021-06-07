#!/usr/bin/env python
# -*- coding: utf-8 -*-
from codecs import open
from os import name as os_name
from os.path import (abspath, dirname, join)
from subprocess import call

from setuptools import (Command, find_packages, setup)

from outd2aclog.version import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


class RunTests(Command):
    """Run all tests."""

    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        err_no = call(['py.test', '--cov=outd2aclog', '--cov-report=term-missing'])
        raise SystemExit(err_no)


class RunBuild(Command):
    """Run pyinstaller build."""

    description = 'run build'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run pyinstaller build."""
        static_sep = ';' if os_name == 'nt' else ':'  # On Windows pyinstaller needs the separator to be ';'
        err_no = call(['pyinstaller', '--name', 'outd2aclog', '--onefile', '--noconsole',
                       '--add-data', 'outd2aclog/static/*{}outd2aclog/static/'.format(static_sep),
                       '--icon', 'outd2aclog/static/outd2aclogicon.ico', 'launch.py'])
        raise SystemExit(err_no)


setup(
    name='OUTD-2-ACLOG',
    version=__version__,
    description='Converts OutD ADIF log files to ACLOG (N3FJP) ADIF parsable log files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/arkorobotics/OUTD_2_ACLOG',
    author='N6ARA',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='outd adif aclog adif parser',
    project_urls={
        'Source': 'https://github.com/arkorobotics/OUTD_2_ACLOG',
        'Tracker': 'https://github.com/arkorobotics/OUTD_2_ACLOG/issues',
    },
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    install_requires=[
        'tk==0.1.0',
        'tkmacosx==1.0.3',
    ],
    python_requires='~=3.9',
    extras_require={
        'build': ['pyinstaller==4.3'],
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    cmdclass={
        'test': RunTests,
        'build': RunBuild,
    },
    entry_points={
        'console_scripts': [
            'outd2aclog=outd2aclog.gui:main',
        ],
    },
)
