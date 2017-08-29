#!/usr/bin/env python
import glob
from setuptools import setup, find_packages
from os.path import join, abspath, dirname

requirements_txt = join(abspath(dirname(__file__)), 'requirements.txt')
requirements = [l.strip() for l in open(requirements_txt) if l and not l.startswith('#')]

version = '0.0.1'


setup(
    name='small-tools',
    version=version,
    packages=find_packages(exclude=('tests',)),
    url='https://github.com/EdinburghGenomics/clarity_scripts',
    license='MIT',
    description='Small python_scripts used to perform various task within Edinburgh Genomics',
    long_description='Small python_scripts used to perform various task within Edinburgh Genomics',
    install_requires=requirements,  # actual module requirements
    scripts=glob.glob("python_scripts/*.py"),
    zip_safe=False,
    author='Timothee Cezard',
    author_email='timothee.cezard@ed.ac.uk'
)
