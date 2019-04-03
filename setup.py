#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='kivy_mt',
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
        'kivy',
        'kivy-garden',
        'pygame', # for kivy
      ]
    )
