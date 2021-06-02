#!/usr/bin/python3
from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Hello world app',
    ext_modules=cythonize("tpf_udp_proxy.pyx"),
    zip_safe=False,
)
