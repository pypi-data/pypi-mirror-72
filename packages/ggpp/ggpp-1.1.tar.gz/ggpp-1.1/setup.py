import os
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="ggpp",
    version="1.1",
    author="Davi Sousa",
    packages=["ggpp"],
    author_email="davi.gomes.sousa@ccc.ufcg.edu.br",
    description=(
        "An useful g++ interface, to run easily C/C++ code on Linux and Windows."),
    license="MIT",
    keywords="c++ cpp c h g++ interface",
    url="https://github.com/davigsousa/ggpp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": ["ggpp=ggpp.main:run"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
