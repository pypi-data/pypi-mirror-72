#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pylokit==0.8.1',
    'django<3.0.0',
    'billiard>=3.5.0.2,<3.6.0',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='jpt-templated-docs',
    version='0.4.0',
    description=('Generate PDF, MS Word and Excel documents from templates '
                 'in Django.'),
    long_description=readme + '\n\n' + history,
    author="Jewel Paymentech",
    author_email='jafnee.jesmee@jewelpaymentech.com',
    url='https://github.com/jptd/templated-docs',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='templateddocs',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests.test_app.tests',
    tests_require=test_requirements
)
