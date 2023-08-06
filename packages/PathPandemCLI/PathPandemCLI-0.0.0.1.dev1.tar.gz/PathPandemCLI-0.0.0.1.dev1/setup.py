#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from setuptools import setup

with open("./LongDescription", 'r') as README_FILE:
    long_description = README_FILE.read()

setup(
    name='PathPandemCLI',
    version='0.0.0.1dev1',
    description='Simulate Pandemic Pathogen Outbreak Non-Gooey version',
    license="GPLv3",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pradyumna Paranjape',
    author_email='pradyparanjpe@rediffmail.com',
    url="",
    packages=['PathPandemCLI'],
    install_requires=['numpy', 'matplotlib'],
    scripts=['bin/PathPandemCLI',],
    package_data={'PathPandemCLI': ['reverse_cfr_database.pkl']},
)
