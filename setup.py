#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='log_generator',
    version='2.0.0',
    description='A command line application to generate logs.',
    long_description=long_description,
    url='',
    author='DobyLov',
    author_email='ricodoby@hotmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Stagging/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    keywords='cli random logs',
    packages=['log_generator'],
    entry_points={
        'console_scripts': [
            'loggen=log_generator:main',
        ],
    },
)
