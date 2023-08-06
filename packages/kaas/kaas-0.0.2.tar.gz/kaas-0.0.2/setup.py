#!/usr/bin/env python3

from setuptools import setup

setup(
    name="kaas",
    version="0.0.2",
    packages=["kaas"],
    long_description="Parse PowerShell PSD1 files",
    url="https://github.com/DavidVentura/kaas",
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=[
        'pyleri==1.3.2',
    ],
    entry_points={"console_scripts": ["psd2json = kaas.cli:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    )
