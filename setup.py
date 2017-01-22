# -*- coding: utf-8 -*-

from __future__ import division

from setuptools import setup, find_packages
import subprocess
import shlex

GIT_HEAD_REV = subprocess.check_output(shlex.split('git rev-parse --short HEAD')).strip()


setup(
    name='django-ribbon',
    version='0.1.dev#%s' % GIT_HEAD_REV,
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/silverfix/django-ribbon',
    license='BSD',
    author='Andrea Rabbaglietti',
    author_email='rabbagliettiandrea@gmail.com',
    description='Ribbon is yet another Stripe manager app',
    install_requires=[
        'django>=1.8',
        'stripe',
        'pygments'
    ]
)
