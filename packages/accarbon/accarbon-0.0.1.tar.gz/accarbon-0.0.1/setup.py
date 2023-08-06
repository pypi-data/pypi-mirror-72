import unittest
from setuptools import setup, find_packages
import sys
from os import path

root_dir = path.abspath(path.dirname(__file__))


def _requirements():
    return [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]


def test_suite():
    sys.path.append('./accarbon_command')
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='test_*.py')
    return test_suite


def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()


setup(
    name='accarbon',
    packages=find_packages(),

    version='0.0.1',

    license='MIT',

    install_requires=_requirements(),

    author='kimitsu',
    author_email='yunosuke@ueda.info.waseda.ac.jp',

    url='https://github.com/YunosukeY/ac-carbon-command',

    description='Tweet images of source code submitted to AtCoder.',
    long_description=read("README.rst"),
    keywords='atcoder carbon',

    test_suite='setup.test_suite',

    entry_points={
        'console_scripts': [
            'accarbon = accarbon_command.main:main',
        ],
    },
)
