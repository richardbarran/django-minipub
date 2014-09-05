#/usr/bin/env python

import os
from setuptools import setup, find_packages

import mininews

ROOT_DIR = os.path.dirname(__file__)


def get_requirements(requirements_file):
    with open(requirements_file) as f:
        required = [line.split('#')[0] for line in f.read().splitlines()]
    return required

setup(
    name='django-mininews',
    version=mininews.__version__,
    packages=find_packages(exclude=['example_project']),
    license='MIT',
    description='Boilerplate for creating publishable lists of objects',
    long_description=open('README.rst').read(),
    install_requires=get_requirements(os.path.join(ROOT_DIR, 'requirements.txt')),
    url='https://github.com/richardbarran/django-mininews',
    author='Richard Barran',
    author_email='richard@arbee-design.co.uk',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
