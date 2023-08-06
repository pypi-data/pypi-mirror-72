# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neatutils']

package_data = \
{'': ['*']}

install_requires = \
['click-help-colors>=0.8,<0.9', 'click>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'neatutils',
    'version': '0.0.1',
    'description': 'NeatUtils - a simple reference utility for awesome lists and machine learning estimators and algorithms',
    'long_description': "### neatutils\nA Simple Reference Utility for Getting the Abbreviation of ML Estimators,Algorithms and Awesome List\n\n### Installation\n```bash\npip install neatutils\n```\n\n### Benefits\n+ Simplify finding ML estimator name for pycaret\n\n### Why Neatutils?\n+ During usage of the powerful ML library Pycaret, I noticed that it was difficult to know which abbreviation/short name can be used each ML Estimator, hence we decided to build something simple to make it easier to know the most common name/abbreviation for most Machine Learning/Data Science Algorithms and Estimators used.\n\n### Usage\n#### Get Abbreviations\n+ Neatutils offers the ability to analyse sequences for more insight\n\n```python\n>>> import neatutils\n>>> neatutils.get_abbrev('Logistic Regression')\n>>> lr\n```\n\n#### Get Full Name of Estimators\n```python\n>>> import neatutils\n>>> neatutils.get_fullname('lr')\n'Logistic Regression'\n\n```\n#### Documentation\n+ Please read the [documentation](https://github.com/Jcharis/neatutils/wiki) for more information on what neatutils does and how to use is for your needs.\n\n#### More Features To Add\n+ awesome list\n+ support for more file formats\n\n\n\n#### Acknowledgements\n   + Inspired by packages like PyCaret,Awesome-hub\n\n### NB\n+ Contributions Are Welcomed\n+ Notice a bug, please let us know.\n+ Thanks A lot\n\n### By\n+ Jesse E.Agbe(JCharis)\n+ Jesus Saves @JCharisTech\n",
    'author': 'Jesse E.Agbe(JCharis)',
    'author_email': 'jcharistech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jcharis/neatutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.3,<4.0',
}


setup(**setup_kwargs)
