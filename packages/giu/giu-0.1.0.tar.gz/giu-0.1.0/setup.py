# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['giu']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'halo>=0.0.29,<0.0.30',
 'requests>=2.24.0,<3.0.0',
 'tomlkit>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['giu = giu.cli:giu']}

setup_kwargs = {
    'name': 'giu',
    'version': '0.1.0',
    'description': 'Commnand line tool to interact with Gandi LiveDNS',
    'long_description': "# GIU\nGandi LiveDNS Updater - commnand line tool to keep your dynamic ip up to date.\n\n## Prequisites\n\n* A valid key fro Gandi LiveDNS API. Use https://account.gandi.net/en/users/USER/security\n(`USER` is your Gandi user account).\n* Python 3.\n\n## Installation\n\nThe recommended way to install this package is through [pip](https://pip.pypa.io/en/stable/).\n\n```shell\npip install --user giu\n```\n\n## Usage\n\nTo use `giu` you need to create a `config.toml` file to hold the minimal set of\nconfigurations.\n\n```toml\n[api]\nurl = 'https://dns.api.gandi.net/api/v5'\nkey = 'YOUR_KEY'\n\n[dns]\ndomain = 'example.com'\nrecords = [\n    {'type' = 'A', 'name' = '@', 'ttl' = 18000},\n]\n\n[resolver]\nproviders = [\n    'http://ipecho.net/plain',\n    'https://ifconfig.me/ip',\n    'http://www.mon-ip.fr'\n]\n```\n\n### One shot\nIn this example the config file was created on `$HOME/.giu/example.com.toml`.\n\n```shell\ngiu sync --conf $HOME/.giu/example.com.toml\n```\n\n### Cronjob\nIn this example the config file was created on `$HOME/.giu/example.com.toml`.\n\n```shell\n$ crontab -e\n* */2 * * * giu sync --conf $HOME/.giu/example.com.toml\n```\n\n## Improvements\n\nSome improvements that I have ff the top of my head:\n\n* `put` command to create entries like CNAMES and so on.\n* `delete` command to delete entries\n* `backup` command to do backups\n* Docker Image to run giu with docker compose or as a Cronjob on Kubernetes.\n",
    'author': 'Yago Riveiro',
    'author_email': 'yago.riveiro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yriveiro/giu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
