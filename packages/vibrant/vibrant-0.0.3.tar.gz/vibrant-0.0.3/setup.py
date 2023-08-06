# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vibrant']

package_data = \
{'': ['*']}

install_requires = \
['pyvista>=0.24,<0.25', 'torch>=1.2,<2.0']

entry_points = \
{'console_scripts': ['clean = scripts:clean',
                     'docs = scripts:docs',
                     'format = scripts:format',
                     'lint = scripts:lint',
                     'retest = scripts:retest',
                     'servedocs = scripts:servedocs',
                     'test = scripts:test']}

setup_kwargs = {
    'name': 'vibrant',
    'version': '0.0.3',
    'description': 'PyTorch powered Finite Elements',
    'long_description': '# Vibrant\n\nPyTorch powered Finite Elements\n\nWarning: Work in progress.\n\n[![Unix Build Status](https://img.shields.io/travis/gcapu/vibrant/master.svg?label=unix)](https://travis-ci.org/gcapu/vibrant)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/gcapu/vibrant/master.svg?label=windows)](https://ci.appveyor.com/project/gcapu/vibrant)\n[![Coverage Status](https://img.shields.io/coveralls/gcapu/vibrant/master.svg)](https://coveralls.io/r/gcapu/vibrant)\n[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/gcapu/vibrant.svg)](https://scrutinizer-ci.com/g/gcapu/vibrant/?branch=master)\n[![PyPI Version](https://img.shields.io/pypi/v/vibrant.svg)](https://pypi.org/project/vibrant)\n[![PyPI License](https://img.shields.io/pypi/l/vibrant.svg)](https://pypi.org/project/vibrant)\n\n## Setup\n\n### Requirements\n\n* Python 3.7+\n\n### Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\npip install vibrant\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\npoetry add vibrant\n```\n\n## Usage\n\nAfter installation, the package can imported:\n\n```text\n$ python\n>>> import vibrant\n>>> vibrant.__version__\n```\n\n## Documentation\n\nFor more information about advanced features, see the official vibrant [documentation](https://gcapu.github.io/).\n',
    'author': 'German Capuano',
    'author_email': 'e@gcapu.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/vibrant',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
