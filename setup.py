#!/usr/bin/env python3
"""
KeyHound Enhanced - Setup Configuration
Professional Bitcoin cryptography platform
"""

from setuptools import setup, find_packages

setup(
    name="keyhound-enhanced",
    version="2.0.0",
    author="KeyHound Development Team",
    author_email="sethpizzaboy@gmail.com",
    description="Enterprise Bitcoin cryptography and puzzle solving platform",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "ecdsa>=0.17.0",
        "base58>=2.1.0",
        "cryptography>=3.4.0",
        "flask>=2.0.0",
        "requests>=2.25.0",
        "psutil>=5.8.0",
        "tqdm>=4.62.0",
        "pyyaml>=5.4.0",
    ],
    entry_points={
        "console_scripts": [
            "keyhound=keyhound.main:main",
        ],
    },
)
