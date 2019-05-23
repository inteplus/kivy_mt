#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='kivy-mt',
      version='0.0.1',
      description="Extra Kivy modules written by Minh-Tri Pham",
      author=["Minh-Tri Pham"],
      #scripts=['scripts/visionml_viewer.py'],
      packages=find_packages(),
      package_data={
        'kivy_mt': ['data/*'],
      },
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'base_mt', # for logging and multi-threading purposes
        'kivy',
        'kivy-garden',
        'pygame', # for kivy
      ],
      dependency_links=[
        'git+https://github.com/inteplus/base_mt#egg=base-mt-0.0.1',
      ]
    )
