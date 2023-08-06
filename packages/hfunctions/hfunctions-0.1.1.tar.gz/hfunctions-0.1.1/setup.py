#!/usr/bin/env python

"""The setup script."""
import pathlib
from setuptools import setup, find_packages

_here = pathlib.Path(__file__).parent

version = (_here / "VERSION").read_text()

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Ahmed Salhin",
    author_email='ahmed@salhin.org',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Handy function for data science work",
    entry_points={
        'console_scripts': [
            'hfunctions=hfunctions.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='hfunctions',
    name='hfunctions',
    packages=find_packages(include=['hfunctions', 'hfunctions.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ahmedsalhin/hfunctions',
    version=version,
    zip_safe=False,
)
