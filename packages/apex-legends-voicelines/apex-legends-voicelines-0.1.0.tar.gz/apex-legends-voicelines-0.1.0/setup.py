# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apex_legends_voicelines', 'apex_legends_voicelines.assets']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['apex-voicelines = apex_legends_voicelines.__main__:main']}

setup_kwargs = {
    'name': 'apex-legends-voicelines',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Justine Kizhakkinedath',
    'author_email': 'justine@kizhak.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
