#!/usr/bin/env python

import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

if sys.version_info < (3, 3):
    sys.exit('Sorry, Python < 3.3 is not supported')


class PyTest(TestCommand):
    def run_tests(self):
        import pytest
        errno = pytest.main([])
        sys.exit(errno)


setup(
    name='pymultigen',
    version='0.0.1',
    description='Multi-file frontend for single-file code generators.',
    long_description=open('README.rst').read(),
    keywords='code generator jinja multi-file',
    url='https://github.com/moltob/pymultigen',
    author='Mike Pagel',
    author_email='mike@mpagel.de',

    packages=find_packages(exclude=['tests']),
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True,
    install_requires=[],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},

    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
    ]
)
