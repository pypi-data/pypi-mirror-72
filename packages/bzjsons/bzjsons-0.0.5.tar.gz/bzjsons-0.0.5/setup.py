#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import codecs
import os

__project_ = 'bzjsons'
__file_name__ = 'setup'
__author__ = 'bright.zhang'
__time__ = '2020/6/23 01:44'


try:
    from setuptools import setup
except ModuleNotFoundError:
    from distutils.core import setup


def read(file_name):
    return codecs.open(os.path.join(os.path.dirname(__file__), file_name)).read()


long_des = read("README.rst")
platforms = ['linux/Windows']
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

install_requires = []

all_modules = [
    'bzjsons',
]

setup(name='bzjsons',
      version='0.0.5',
      keywords=('json', 'serialize', 'deserialize', '序列化', '反序列化'),
      description='A enhanced json utility based upon json.',
      long_description=long_des,
      py_modules=all_modules,
      author="Bright Zhang",
      author_email="67669182@qq.com",
      url="https://gitee.com/brightzh/bzjsons/",
      license="MIT",
      platforms=platforms,
      classifiers=classifiers,
      install_requires=install_requires,
      zip_safe=False,
      )
