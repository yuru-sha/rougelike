"""
Setup configuration for the Rogue game
"""
from setuptools import setup, find_packages

setup(
    name="roguelike",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "blessed==1.20.0",
        "injector==0.21.0",
    ],
    python_requires=">=3.8",
    author="yuru-sha",
    description="A Rogue-like game implementation",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 