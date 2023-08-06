#!/usr/bin/env python3

from setuptools import find_packages, setup

INSTALL_REQUIRES = ['numpy']
TESTS_REQUIRE = []

setup(
    name='franklab_mstaggedcuration',
    version='0.1.3.dev0',
    license='',
    description=(''),
    author='',
    author_email='',
    url='',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    include_package_data=True,
)
