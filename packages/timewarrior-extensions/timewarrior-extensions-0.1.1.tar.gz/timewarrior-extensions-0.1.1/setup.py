# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timewarrior_extensions']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['timewarrior_percentage_install = '
                     'timewarrior_extensions.install:install_percentage']}

setup_kwargs = {
    'name': 'timewarrior-extensions',
    'version': '0.1.1',
    'description': 'Extensions for Timewarrior',
    'long_description': '# timewarrior-extensions\nExtensions for [Timewarrior](https://timewarrior.net/)\n\n## Installation\nInstall the extensions\n\n```sh\n  pip install --user timewarrior-extensions\n```\nAnd install extensions you want\n\n## Extensions\n### Percentage\nTime report with %\n\n#### Installation\n```\ntimewarrior_percentage_install\n```\n\n#### Usage\n```sh\n  timew percentage\n  timew percentage :day\n  timew percentage :week\n  timew percentage :lastweek\n  timew percentage :month\n```\n\n#### Output\n```\nTag             Duration  Portion\n--------------  --------  -------\nMulti word tag  3:00       44.9%\ndevelopment     1:31       22.8%\nmeeting         1:00       15.0%\nreview          1:00       15.0%\nS2              0:08        2.1%\nS               0:01        0.2%\n--------------  --------  -------\nTotal           6:40      100.0%\n```\n\n## Development\n\n```sh\n  git clone https://github.com/ViliamV/timewarrior-extensions.git\n  cd timewarrior-extensions\n  poetry install\n  ln -rs pre-commit .git/hooks/\n```\n',
    'author': 'Viliam Valent',
    'author_email': 'viliam@valent.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ViliamV/timewarrior-extensions',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
