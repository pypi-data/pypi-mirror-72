# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['container_env']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'container-env',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Container Env\n\nEnvironment variables are the easiest way to manage options in containers.\nEspecially when using Docker Swarm or Kubernetes.\nContainer Env makes it easy to create applications with environment based\nconfiguration.\n\n* Simple. Can be picked up in minutes.\n* Easy to use with Django, Flask and others.\n* Seamless support for secrets.\n* Built with container orchestration in mind.\n\n[Visit the website](https://lkummer.github.io/container-env/) for more information.\n\n## Getting Started\n\nPython 3.8 or higher is required.\n\n[See the quick start guide](https://lkummer.github.io/container-env/guide/quickstart/)\nto get started.\n\n## Usage\n\n[See the documentation](http://localhost:1313/container-env/guide/)\nto learn more about Container Env.\n\n## Contributing\n\nPlease [check existing issues](https://github.com/LKummer/container-env/issues)\nbefore opening a new one.\n\n[See the development guide](https://lkummer.github.io/container-env/guide/development/)\nto learn about the development setup.\n',
    'author': 'Lior Kummer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lkummer.github.io/container-env/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
