# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jellyfin_accounts']

package_data = \
{'': ['*'],
 'jellyfin_accounts': ['data/*', 'data/static/*', 'data/templates/*']}

install_requires = \
['flask-httpauth>=3.3.0',
 'flask>=1.1.2,<2.0.0',
 'itsdangerous>=1.1.0,<2.0.0',
 'packaging>=20.4,<21.0',
 'passlib>=1.7.2,<2.0.0',
 'pyopenssl>=19.1.0,<20.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2020.1,<2021.0',
 'requests>=2.23.0,<3.0.0',
 'waitress>=1.4.3,<2.0.0',
 'watchdog>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['jf-accounts = jellyfin_accounts:main']}

setup_kwargs = {
    'name': 'jellyfin-accounts',
    'version': '0.2.6',
    'description': 'A simple account management system for Jellyfin',
    'long_description': '# ![jellyfin-accounts](https://raw.githubusercontent.com/hrfee/jellyfin-accounts/master/images/jellyfin-accounts-banner-wide.svg)\n\nA basic account management system for [Jellyfin](https://github.com/jellyfin/jellyfin).\n* Provides a web interface for creating invite codes, and a simple account creation form\n* Sends out emails when a user requests a password reset\n* Uses a basic python jellyfin API client for communication with the server. \n* Uses [Flask](https://github.com/pallets/flask), [HTTPAuth](https://github.com/miguelgrinberg/Flask-HTTPAuth), [itsdangerous](https://github.com/pallets/itsdangerous), and [Waitress](https://github.com/Pylons/waitress)\n* Frontend uses [Bootstrap](https://getbootstrap.com), [jQuery](https://jquery.com) and [jQuery-serialize-object](https://github.com/macek/jquery-serialize-object)\n* Password resets are handled using smtplib, requests, and [jinja](https://github.com/pallets/jinja)\n## Interface\n<p align="center">\n    <img src="https://raw.githubusercontent.com/hrfee/jellyfin-accounts/master/images/jfa.gif" width="100%"></img>\n</p>\n\n<p align="center">\n    <img src="https://raw.githubusercontent.com/hrfee/jellyfin-accounts/master/images/jfa.gif" width="48%" style="margin-right: 1.5%;" alt="Admin page"></img> \n    <img src="https://raw.githubusercontent.com/hrfee/jellyfin-accounts/master/images/create.png" width="48%" style="margin-left: 1.5%;" alt="Account creation page"></img>\n</p>\n\n\n\n## Get it\n### Requirements\n\n* This should work anywhere Python does, i\'ve tried to not use anything OS-specific. Drop an issue if there\'s a problem, of course.\n```\n* python >= 3.6\n* flask\n* flask_httpauth\n* jinja2\n* requests\n* itsdangerous\n* passlib\n* pyOpenSSL\n* waitress\n* pytz\n* python-dateutil\n* watchdog\n* packaging\n```\n### Install\n\nUsually as simple as:\n```\npip install jellyfin-accounts\n```\nIf not, or if you want to use docker, see [install](https://github.com/hrfee/jellyfin-accounts/wiki/Install).\n\n## Usage\n* Passing no arguments will run the server\n```\nusage: jf-accounts [-h] [-c CONFIG] [-d DATA] [--host HOST] [-p PORT] [-g]\n\njellyfin-accounts\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c CONFIG, --config CONFIG\n                        specifies path to configuration file.\n  -d DATA, --data DATA  specifies directory to store data in. defaults to\n                        ~/.jf-accounts.\n  --host HOST           address to host web ui on.\n  -p PORT, --port PORT  port to host web ui on.\n  -g, --get_defaults    tool to grab a JF users policy (access, perms, etc.)\n                        and homescreen layout and output it as json to be used\n                        as a user template.\n```\n## Setup\n#### New user template\n* You may want to restrict a user from accessing certain libraries (e.g 4K Movies), display their account on the login screen by default, or set a default homecrseen layout. Jellyfin stores these settings in the user\'s policy, configuration and displayPreferences.\n* Make a temporary account and configure it, then in the web UI, go into "Settings => Set new account defaults". Choose the account, and its configuration will be stored for future use.\n#### Emails/Password Resets\n* When someone initiates forget password on Jellyfin, a file named `passwordreset*.json` is created in its configuration directory. This directory is monitored and when created, the program reads the username, expiry time and PIN, puts it into a template and sends it to whatever address is specified in `emails.json`.\n* **The default forget password popup references the `passwordreset*.json` file created. This is confusing for users, so a quick fix is to edit the `MessageForgotPasswordFileCreated` string in Jellyfin\'s language folder.**\n* Currently, jellyfin-accounts supports generic SSL/TLS or STARTTLS secured SMTP, and the [mailgun](https://mailgun.com) REST API. \n* Email html is created using [mjml](https://mjml.io), and [jinja](https://github.com/pallets/jinja) templating is used. If you wish to create your own, ensure you use the same jinja expressions (`{{ pin }}`, etc.) as used in `data/email.mjml` or `invite-email.mjml`, and also create plain text versions for legacy email clients.\n\n### Configuration\n* Note: Make sure to put this behind a reverse proxy with HTTPS.\n\nOn first run, access the setup wizard at `0.0.0.0:8056`. When finished, restart the program.\n\nThe configuration is stored at `~/.jf-accounts/config.ini`. Settings can be changed through the web UI, or by manually editing the file.\n\nFor detailed descriptions of each setting, see [setup](https://github.com/hrfee/jellyfin-accounts/wiki/Setup).\n\n### Donations\nI strongly suggest you send your money to [Jellyfin](https://opencollective.com/jellyfin) or a good charity, but for those who want to help me out, a Paypal link is below.\n\n[Donate](https://www.paypal.me/hrfee)\n',
    'author': 'Harvey Tindall',
    'author_email': 'harveyltindall@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hrfee/jellyfin-accounts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
