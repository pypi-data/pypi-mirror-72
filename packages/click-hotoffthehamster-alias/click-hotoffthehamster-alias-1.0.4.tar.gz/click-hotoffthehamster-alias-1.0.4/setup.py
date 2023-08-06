#!/usr/bin/env python

from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='click-hotoffthehamster-alias',
    version='1.0.4',
    description='Add aliases to click-hotoffthehamster commands',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Hot Off The Hamster',
    author_email='hotoffthehamster@gmail.com',
    url='https://github.com/hotoffthehamster/click-hotoffthehamster-alias',
    license='MIT',
    packages=['click_hotoffthehamster_alias'],
    install_requires=[
        'click-hotoffthehamster >= 7.1.1 , < 8',
    ],
    extras_require={
        'dev': [
            'flake8',
            'flake8-import-order',
            'tox-travis',
            'pytest >= 5.4.3',
            'pytest-cov >= 2.10.0',
            'coveralls',
            'wheel',
        ]
    }
)
