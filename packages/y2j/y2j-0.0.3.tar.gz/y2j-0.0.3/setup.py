#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='y2j',
    version='0.0.3',
    author='Neal Ormsbee',
    author_email='neal.ormsbee@gmail.com',
    description='A CLI tool for converting YAML to JSON.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SheepGotoHeaven/y2j',
    install_requires=['pyyaml'],
    packages=find_packages(),
    license='MIT',
    zip_safe=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'y2j = y2j.__main__:main'
        ]
    }
)
