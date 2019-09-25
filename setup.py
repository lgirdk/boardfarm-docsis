#!/usr/bin/env python


from setuptools import setup, find_packages

setup(name='boardfarm_docsis',
      version='1.0.0',
      description='An add-on to boardfarm that contains DOCSIS specific tests and libraries',
      author='Various',
      url='https://github.com/lgirdk/boardfarm-docsis',
      packages=find_packages(),
      package_data={'': ['*.txt','*.json','*.cfg','*.md','*.mib','*.tcl']},
      include_package_data=True
     )
