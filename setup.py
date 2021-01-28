#!/usr/bin/python3
import os
import subprocess

import setuptools

from notes.notes import _version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="notes-cli",
    version=_version,
    author="Merlin Roe",
    author_email="merlin.roe@hotmail.co.uk",
    description="A basic CLI notes tool using Markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/merlinr/CLI_notes",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["notes=notes.notes:main"]},
    install_requires=["mdv"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
