#! -*- coding: utf-8 -*-
from setuptools import setup

setup(name='soran',
      version='0.0.1',
      author='Kang Hyojun',
      author_email='hyojun@admire.kr',
      install_requires=[
          'flask==0.10.1', 'flask-script==0.5.3', 'sqlalchemy==0.8.3',
          'Flask-OAuthlib==0.3.0', 'alembic==0.6.0', 'pytest==2.3.5',
          'py-bcrypt==0.4', 'simplejson==3.3.1', 'lxml==3.2.3'
      ])
