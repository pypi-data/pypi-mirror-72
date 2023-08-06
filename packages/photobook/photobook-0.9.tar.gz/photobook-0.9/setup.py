#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='photobook',
    version='0.9',
    description='Built photobook with python',
    author='Benjamin Bertrand',
    author_email='benjamin.bertrand@opytex.org',
    url='https://git.opytex.org/lafrite/photobook.git',
    packages=find_packages(),
    include_package_data = True,
    install_requires=[
        "fpdf",
        "Pillow",
    ],
    )
