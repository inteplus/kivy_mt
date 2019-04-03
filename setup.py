#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='muv1',
      version='0.4.1',
      description="Winnow Vision dataset loader and viewer",
      author=["Phong Dinh Vo", "Minh-Tri Pham"],
      scripts=['scripts/visionml_viewer.py'],
      packages=find_packages(),
      package_data={
        'muv1.viewer': ['data/*'],
      },
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'mlcore>=0.4.6',
        'numpy',
        'pandas',
        'Cython', # for taxtree
        #'sshtunnel', # for accessing Winnow home
        #'pygame', # for kivy
        #'kivy', # should still work without kivy
        #'tornado', # for rapidly serving event images
      ]
    )
