from setuptools import setup, find_packages

setup(
    name='django-mininews',
    version='0.1',
    packages=find_packages(exclude=['example_project']),
    license='MIT',
    description='Boilerplate for creating publishable lists of objects',
    long_description=open('README.rst').read(),
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
