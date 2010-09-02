#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argue

from distutils.core import setup


def publish():
	"""Publish to PyPi"""
	os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
	publish()
	sys.exit()

setup(
	name='argue',
	version=argue.__version__,
	description='Python apps deserve a good argument!',
	long_description=open('README.rst').read() + '\n\n' + open('HISTORY.rst').read(),
	author='Kenneth Reitz',
	author_email='me@kennethreitz.com',
	url='http://github.com/kennethreitz/argue',
	packages=['argue'],
	license='MIT',
	classifiers=(
		""
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2.5",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
	)
)
