#/usr/bin/env python

import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements

import minipub


def get_requirements(source):
    try:
        install_reqs = parse_requirements(source, session=uuid.uuid1())
    except TypeError:
        # Older version of pip.
        install_reqs = parse_requirements(source)
    return list(set([str(ir.req) for ir in install_reqs]))


setup(
    name='django-minipub',
    version=minipub.__version__,
    packages=find_packages(exclude=['example_project']),
    include_package_data=True,
    license='MIT',
    description='Django-minipub is a MINImalist PUBlication control system for Django.',
    long_description=open('README.rst').read(),
    install_requires=get_requirements('requirements.txt'),
    url='https://github.com/richardbarran/django-minipub',
    author='Richard Barran',
    author_email='richard@arbee-design.co.uk',
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
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
