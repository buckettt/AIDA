# -*- coding: utf-8 -*-

from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("natvent.pyx"),
)