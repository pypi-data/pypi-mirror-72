#!/usr/bin/env python
# -*- coding: utf-8 -*-


import setuptools

from pbr.packaging import parse_requirements


entry_points = {
}


setuptools.setup(
    name='placementclient',
    version='0.3.0',
    description=('Client for the Placement API'),
    author='Sam Morrison',
    author_email='sorrison@gmail.com',
    url='https://github.com/NeCTAR-RC/python-placementclient',
    packages=[
        'placementclient',
    ],
    include_package_data=True,
    install_requires=parse_requirements(),
    license="Apache",
    zip_safe=False,
    classifiers=(
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ),
    entry_points=entry_points,
)
