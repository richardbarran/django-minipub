from setuptools import setup, find_packages

setup(
    name='django-mininews',
    version='0.1',
    packages=find_packages(exclude=['example_project']),
    license='MIT',
    description='Boilerplate for creating publishable lists of objects',
    long_description=open('README.rst').read(),
    author='Richard Barran',
    author_email='richard@arbee-design.co.uk',
)
