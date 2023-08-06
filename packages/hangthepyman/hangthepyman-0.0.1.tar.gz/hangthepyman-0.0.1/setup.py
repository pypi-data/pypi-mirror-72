# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hangthepyman']

package_data = \
{'': ['*']}

install_requires = \
['pygame>=1.9.6,<2.0.0']

setup_kwargs = {
    'name': 'hangthepyman',
    'version': '0.0.1',
    'description': '\x16Classic Hangman game with Pygame & Python touch',
    'long_description': "# HangThePyMan\n\n> Classic Hangman game with Pygame & Python touch.\n\nImplementation of the hangman game in Pygame. With the ability to ask today's word, most used & searched words and bunch of other fun options to play.\n\n![screen1](screenshots/screen1.png)\n\n## Installation\n\nPip:\n\n```sh\npip install hangthepyman --user\n```\n\nSource:\n\nAfter cloning head to hangthepyman directory and run:\n\n```sh\npython3 the_hangman.py\n```\n\n## TODO's\n\n- Add Menu\n- Add Music\n- Complete word functions to improve asked words and add hint option\n\n## Release History\n\n- 0.0.1\n  - Created the game :)\n\n## Meta\n\nBerkay Girgin – [@Gerile3](https://github.com/Gerile3) – berkay.grgn@protonmail.com\n\nDistributed under the MIT license. See ``LICENSE`` for more information.\n\n## Contributing\n\n1. Fork it (<https://github.com/Gerile3/HangThePyMan/fork>)\n2. Create your feature branch (`git checkout -b feature/fooBar`)\n3. Commit your changes (`git commit -am 'Add some fooBar'`)\n4. Push to the branch (`git push origin feature/fooBar`)\n5. Create a new Pull Request\n",
    'author': 'Berkay Girgin',
    'author_email': 'berkay.grgn@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Gerile3/HangThePyMan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
