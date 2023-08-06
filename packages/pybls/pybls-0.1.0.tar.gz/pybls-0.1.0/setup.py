#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'requests>=2.24.0']

setup_requirements = [
    'pytest-runner',
    'flake8>=3.8.3',
    'mock>=4.0.2',
    'mypy>=0.782',
    'pytest>=3',
    'pytest-cov>=2.10.0'
]

test_requirements = [
    'flake8>=3.8.3',
    'mock>=4.0.2',
    'mypy>=0.782',
    'pytest>=3',
    'pytest-cov>=2.10.0'
]

setup(
    author="Leon Kozlowski",
    author_email='leonkozlowski@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python client for BLS data",
    entry_points={
        'console_scripts': [
            'pybls=pybls.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pybls',
    name='pybls',
    packages=find_packages(include=['pybls', 'pybls.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/leonkozlowski/pybls',
    version='0.1.0',
    zip_safe=False,
)
