# coding: utf-8
"""Setup script for resnet50 demo by IVA TECH."""

from setuptools import find_packages, setup

setup(name='iva_classification_demo',
      version='1.1.0',
      url='https://iva-tech.ru/',
      author='Alexeev Eugene',
      author_email='e.alekseev@iva-tech.ru',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      entry_points={
            'console_scripts': ['iva_classes_demo=iva_classification_demo.main:main'],
      },
      install_requires=[
            'iva_applications',
            'iva_tpu',
            'qtmodern',
            'tensorflow==1.15.0',
            'keras==2.2.4',
            'Cython',
            'PyQt5',
            'PyQt5-sip',
            'pyqtgraph'
     ])
