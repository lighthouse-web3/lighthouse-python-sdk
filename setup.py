#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="lighthouseweb3",
    version="0.0.1",
    description="Lighthouse Python SDK",
    author="Perfection Loveday",
    author_email="perfection@lighthouse.storage",
    url="https://github.com/lighthouse-web3/lighthouse-python-sdk",
    packages=find_packages("lighthouseweb3"),
    install_requires=["requests"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="lighthouse storage sdk python filecoin ipfs web3 perpetual",
)
