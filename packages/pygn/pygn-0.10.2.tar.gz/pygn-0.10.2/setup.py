#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

from __future__ import absolute_import
from mail2news import VERSION, DESC
import os.path
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='pygn',
      version=VERSION,  # the current Debian version is 0.9.8
      author="Cosimo Alfarano, Matej Cepl",
      author_email="kalfa@debian.org, mcepl@cepl.eu",
      description=DESC,
      long_description=read('README'),
      url='https://gitlab.com/mcepl/pyg',
      py_modules=['mail2news', 'news2mail', 'whitelist', 'wlp',
                  'wlp_parser'],
      test_suite="test",
      scripts=['pygm2n', 'pygn2m'],
      requires=['rply'],
      license="GPLv3",
      keywords=["nntp", "email", "gateway"],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Intended Audience :: System Administrators',
          'Topic :: Utilities',
          'Topic :: Communications :: Usenet News',
          'Environment :: Console',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
      ]
      )
