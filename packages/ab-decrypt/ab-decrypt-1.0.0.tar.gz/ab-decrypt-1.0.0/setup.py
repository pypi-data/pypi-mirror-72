# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ab_decrypt']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.9.2,<3.0.0']

entry_points = \
{'console_scripts': ['ab-decrypt = ab_decrypt.cli:main']}

setup_kwargs = {
    'name': 'ab-decrypt',
    'version': '1.0.0',
    'description': 'Decryptor for android backups',
    'long_description': 'Android Backup Decryptor\n========================\nDecryptor for android backups that were created with ``adb backup``.\n\nInstallation\n------------\n.. code-block:: bash\n\n    python3 -m venv /path/to/venv\n    /path/to/venv/pip install ab-decrypt\n    ln -sr /path/to/venv/ab-decrypt ~/bin/\n\nUsage\n-----\n.. code-block:: bash\n\n    # Read from stdin, write to stdout\n    $ ab-decrypt\n\n    # Read from stdin, write to stdout\n    $ ab-decrypt - -\n\n    # Read from file, write to other file\n    $ ab-decrypt backup.ab backup.tar\n\n    # List backup contents\n    $ ab-decrypt backup.ab | tar -tv\n\nEnvironment variables\n---------------------\n* ``AB_DECRYPT_PASSWORD``: Decryption password\n\nHelp / Bugs / Contributions\n---------------------------\nPlease file an issue or pull request at GitHub.\n',
    'author': 'Jörn Heissler',
    'author_email': 'nosuchaddress@joern.heissler.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joernheissler/ab-decrypt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
