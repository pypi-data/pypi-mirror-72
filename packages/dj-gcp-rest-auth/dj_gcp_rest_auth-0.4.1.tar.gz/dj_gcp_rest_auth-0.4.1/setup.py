#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [ "google-auth>=1.18.0", "django>=3.0.7", "djangorestframework-simplejwt>=4.4.0", "djangorestframework==3.11.0" ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Steve Graham",
    author_email='stgraham2000@gmail.com',
    python_requires='>=3.4',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Permissions class for testing a request is coming from an authorized GCP user.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='dj_gcp_rest_auth',
    name='dj_gcp_rest_auth',
    packages=find_packages(include=['dj_gcp_rest_auth', 'dj_gcp_rest_auth.*']),
    setup_requires=setup_requirements,
    url='https://gitlab.com/pennatus/dj_gcp_rest_auth',
    version='0.4.1',
    zip_safe=False,
)
