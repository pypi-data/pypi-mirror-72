#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup


def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()


def get_packages(package):
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name='gqlbff-postgres',
    version='0.0.2',
    author='Max Ponomarev',
    author_email='ponomarev1802@mail.ru',
    url='https://github.com/PonomarevMaksim/bff-graphql-postgres-client',
    python_requires=">=3.7",
    install_requires=[
        "asyncpg==0.18.3",
        "ujson==1.35",
    ],
    license="BSD",
    description="The web framework",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=get_packages("bffpostgres"),
    include_package_data=True,
    data_files=[("", ["LICENSE"])],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
)
