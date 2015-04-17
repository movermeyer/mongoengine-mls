#!/usr/bin/env python
from os.path import dirname, abspath, join
from setuptools import setup

here = abspath(dirname(__file__))
readme = open(join(here, "README.rst"))

setup(
    name="mongoengine-mls",
    version="1.1.0",
    py_modules=["mongoengine_mls"],
    url="https://github.com/rembish/mongoengine-mls",
    license="BSD",
    author="Aleksey Rembish",
    author_email="alex@rembish.org",
    description="MultiLingualField for MongoEngine",
    long_description="".join(readme.readlines()),
    install_requires=["mongoengine", "mls", "pymongo<3.0"],
    test_suite="tests",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]
)
