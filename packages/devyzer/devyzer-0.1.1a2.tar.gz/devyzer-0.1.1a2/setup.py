#!/usr/bin/env python
import io
import re

from setuptools import setup, find_packages

with io.open('./devyzer/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

with io.open('README.md', encoding='utf8') as readme:
    long_description = readme.read()

setup(
    name='devyzer',
    version=version,
    description='Devyzer CLI',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ayham Hassan',
    author_email='ayham@devyzer.io',
    license='Other',
    url="https://devyzer.io",
    packages=find_packages(
        exclude=[
            'docs', 'tests',
            'windows', 'macOS', 'linux',
            'iOS', 'android',
            'django'
        ]
    ),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Other',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'devyzer = devyzer.main:main',
        ],
    },
    options={
        'app': {
            'formal_name': 'Devyzer',
            'bundle': 'io.devyzer'
        },

        # Desktop/laptop deployments
        'macos': {
            'app_requires': [
            ]
        },
        'linux': {
            'app_requires': [
            ]
        },
        'windows': {
            'app_requires': [
            ]
        },

        # Mobile deployments
        'ios': {
            'app_requires': [
            ]
        },
        'android': {
            'app_requires': [
            ]
        },

        # Web deployments
        'django': {
            'app_requires': [
            ]
        },
    }
)