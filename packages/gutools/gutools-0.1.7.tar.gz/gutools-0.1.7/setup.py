#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as file:
    readme = file.read()

with open('HISTORY.rst') as file:
    history = file.read()


requirements = [
    'Click',
    'PyYAML',
    'codenamize',
    'coloredlogs',
    'graphviz',
    'lockfile',
    'loganalyzer',
    'pandas',
    'parse',
    'psutil',
    'pytest',
    'python_daemon',
    'python_dateutil',
    'setuptools',
    'typing',
    'ujson',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Asterio",
    author_email='asterio.gonzalez@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Univeral Tools for programing",
    entry_points={
        'console_scripts': [
            'gutools=gutools.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='gutools',
    name='gutools',
    packages=find_packages(include=['gutools']),
    package_data={
        '': ['*.txt'],
    },
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/asteriogonzalez/gutools',
    version='0.1.7',
    zip_safe=False,
)
