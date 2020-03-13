#!/usr/bin/env python

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

# requirements
install_requires = ["aiohttp", "py_ecc~=1.7", "toml"]
dev_requires = ["ipdb", "ipython"]
docs_requires = ["Sphinx"]
tests_requires = [
    "black",
    "coverage",
    "flake8",
    "flake8-import-order",
    "pep8-naming",
    "pytest",
    "pytest-aiohttp",
    "pytest-cov",
]
extras_require = {
    "dev": dev_requires + docs_requires + tests_requires,
    "docs": docs_requires,
    "tests": tests_requires,
    "requests": "requests",
}

setup(
    author="Sylvain Bellemare",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Python client for drand.",
    install_requires=install_requires,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="drand",
    name="drand",
    packages=find_packages(include=["drand", "drand.*"]),
    url="https://github.com/initc3/drand.py",
    version="0.1.0.dev3",
    zip_safe=False,
    extras_require=extras_require,
)
