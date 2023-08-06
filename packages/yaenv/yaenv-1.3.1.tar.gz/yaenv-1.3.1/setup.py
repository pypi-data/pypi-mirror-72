# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaenv']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['cached-property>=1.5.1,<2.0.0']}

setup_kwargs = {
    'name': 'yaenv',
    'version': '1.3.1',
    'description': 'Yet another dotenv parser for Python.',
    'long_description': 'yaenv\n=====\n\n|pypi| |rtd| |travis| |codecov|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/yaenv/1.3.1.svg?logo=python\n   :target: https://pypi.org/project/yaenv/1.3.1/\n   :alt: PyPI\n\n.. |rtd| image:: https://img.shields.io/readthedocs/yaenv/v1.3.1.svg?logo=read-the-docs\n   :target: https://yaenv.readthedocs.io/en/latest/v1.3.1/\n   :alt: Read the Docs\n\n.. |travis| image:: https://img.shields.io/travis/ObserverOfTime/yaenv/py3.7.svg?logo=travis\n   :target: https://travis-ci.org/ObserverOfTime/yaenv\n   :alt: Travis CI\n\n.. |codecov| image:: https://img.shields.io/codecov/c/gh/ObserverOfTime/yaenv/py3.7.svg?logo=codecov\n   :target: https://codecov.io/gh/ObserverOfTime/yaenv/branch/py3.7\n   :alt: Codecov\n\nBecause none of the dozen dotenv parsers for Python fit all my use cases.\n\nInstallation\n------------\n\n.. code:: sh\n\n   pip install yaenv\n\nUsage\n-----\n\nDocumentation and examples are available on\n`Read the Docs <https://yaenv.rtfd.io>`_.\n\nSimilar projects\n----------------\n\n* `python-dotenv <https://github.com/theskumar/python-dotenv>`_\n* `django-environ <https://github.com/joke2k/django-environ>`_\n* `django-dotenv <https://github.com/jpadilla/django-dotenv>`_\n* `environs <https://github.com/sloria/environs>`_\n* `envparse <https://github.com/rconradharris/envparse>`_\n\nLicense\n-------\n\n`BSD 3-Clause License <LICENSE>`_\n',
    'author': 'ObserverOfTime',
    'author_email': 'chronobserver@disroot.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ObserverOfTime/yaenv',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
