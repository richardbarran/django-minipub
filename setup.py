#/usr/bin/env python

import minipub

from setuptools import setup, find_packages

with open('requirements.txt') as file:
    reqs = [line for line in file.readlines() if not line.strip().startswith('#')]

setup(
    name='django-minipub',
    version=minipub.__version__,
    packages=find_packages(exclude=['example_project']),
    include_package_data=True,
    license='MIT',
    description='Django-minipub is a MINImalist PUBlication control system for Django.',
    long_description=open('README.rst').read(),
    install_requires=reqs,
    url='https://github.com/richardbarran/django-minipub',
    author='Richard Barran',
    author_email='richard@arbee.design',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
