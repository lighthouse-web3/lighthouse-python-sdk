#!/usr/bin/env python3
import pathlib
from setuptools import setup, find_packages

setup(
    name="lighthouse-web3/Lighthouse-Python-SDK",
    version="0.1.6",
    license="GNU GENERAL PUBLIC LICENSE",
    description="Lighthouse Python SDK",
    author="Ravish Sharma | Ayobami Oki | Nandit Mehra",
    author_email="nandit123@lighthouse.storage",
    url="https://github.com/lighthouse-web3/lighthouse-python-sdk",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["requests"],
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="lighthouse storage sdk python filecoin ipfs web3 perpetual",
    long_description=(
        (pathlib.Path(__file__).parent.resolve()) / "README.md"
    ).read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
)
