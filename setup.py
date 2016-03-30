#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(name='status',
      description='A lightweight HTTP server that shows the status of the machine.',
      author='Michael Bryan',
      packages=find_packages(exclude=['docs', 'scripts']),
      install_requires=[
          'flask',
          'flask-bootstrap',
          'flask-script',
          'flask-moment',
          'flask-sqlalchemy',
          'flask-mail',
          'flask-login',
          'flask-wtf',
          'flask-migrate',
          'psycopg2',
          'requests',
          'bs4',
          'psutil',
      ],
      license='MIT',
     )

