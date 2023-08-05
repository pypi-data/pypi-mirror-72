#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
import platform
import os
from subprocess import check_call

from setuptools import setup, find_packages
import versioneer

pkg_name = 'nbsafety'


def _post_install_hook():
    python_command_suffix = ''
    if platform.system().lower().startswith('win'):
        python_command_suffix = '.exe'
    check_call(f'python{python_command_suffix} -m {pkg_name}.install'.split())


atexit.register(_post_install_hook)


def read_file(fname):
    with open(fname, 'r', encoding='utf8') as f:
        return f.read()


history = read_file('HISTORY.rst')
requirements = read_file('requirements.txt').strip().split()
setup(
    name=pkg_name,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Stephen Macke',
    author_email='stephen.macke@gmail.com',
    description='Fearless interactivity for Jupyter notebooks.',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/nbsafety-project/nbsafety',
    packages=find_packages(exclude=[
        'binder',
        'docs',
        'scratchspace',
        'notebooks',
        'img',
        'test',
        'scripts',
        'markdown',
        'versioneer.py',
        'frontend',
        'blueprint.json',
    ]),
    include_package_data=True,
    install_requires=requirements,
    license='BSD-3-Clause',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)

# python setup.py sdist bdist_wheel --universal
# twine upload dist/*
