# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VAgent_VERSION = '0.0.1'

if __name__ == "__main__":
    setup(
        name = 'src',
        version = VAgent_VERSION,
        packages = find_packages(),
        long_description=__doc__,
        description = 'src common lib',
        include_package_data = True,
        zip_safe = False
    ) 
