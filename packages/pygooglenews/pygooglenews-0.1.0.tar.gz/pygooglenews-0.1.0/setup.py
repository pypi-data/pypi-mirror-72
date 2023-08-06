# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygooglenews']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'dateparser>=0.7.6,<0.8.0',
 'feedparser>=5.2.1,<6.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'pygooglenews',
    'version': '0.1.0',
    'description': 'If Google News had a Python library',
    'long_description': '# pygooglenews\nIf Google News had a Python library\n',
    'author': 'kotartemiy',
    'author_email': 'bugara.artem@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.newscatcherapi.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
