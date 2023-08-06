# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['carto_bq_tiler']
install_requires = \
['Shapely>=1.7.0,<2.0.0',
 'click-spinner>=0.1.10,<0.2.0',
 'click>=7.1.2,<8.0.0',
 'google-cloud-bigquery-storage[fastavro]>=0.8.0,<0.9.0',
 'google-cloud-bigquery>=1.24.0,<2.0.0',
 'grpcio>=1.28.1,<2.0.0',
 'mercantile>=1.1.4,<2.0.0',
 'pyproj==2.5.0']

entry_points = \
{'console_scripts': ['carto_bq_tiler = carto_bq_tiler:main']}

setup_kwargs = {
    'name': 'carto-bq-tiler',
    'version': '0.1.0rc0',
    'description': 'CARTO BigQuery Tiler cli',
    'long_description': None,
    'author': 'CARTO',
    'author_email': 'support@carto.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5.3,<4.0.0',
}


setup(**setup_kwargs)
