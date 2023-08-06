# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lambda_generator',
 'lambda_generator.templates.python_serverless_docker_jenkins',
 'lambda_generator.templates.python_serverless_docker_jenkins.tests']

package_data = \
{'': ['*'],
 'lambda_generator.templates.python_serverless_docker_jenkins': ['dockers/*']}

install_requires = \
['python-decouple>=3.3,<4.0',
 'pyyaml==5.3.1',
 'sentry_sdk>=0.15.0,<0.16.0',
 'typer>=0.3.0,<0.4.0',
 'yamllint>=1.23.0,<2.0.0']

entry_points = \
{'console_scripts': ['lambda = lambda_generator.cli:main']}

setup_kwargs = {
    'name': 'lambda-generator',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'matheusfrancisco',
    'author_email': 'matheusmachadoufsc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
