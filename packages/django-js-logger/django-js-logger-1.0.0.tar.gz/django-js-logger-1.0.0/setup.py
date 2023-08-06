# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_js_logger']

package_data = \
{'': ['*'], 'django_js_logger': ['static/django_js_logger/*']}

install_requires = \
['django>=2.2,<4.0', 'djangorestframework>=3,<4']

setup_kwargs = {
    'name': 'django-js-logger',
    'version': '1.0.0',
    'description': 'Frontend logging for Django projects',
    'long_description': '========================\nDjango Javascript Logger\n========================\n\n.. image:: https://img.shields.io/pypi/v/django-js-logger.svg\n    :target: https://pypi.org/project/django-js-logger/\n\n.. image:: https://img.shields.io/pypi/pyversions/django-js-logger.svg\n    :target: https://pypi.org/project/django-js-logger/\n\n.. image:: https://img.shields.io/pypi/djversions/django-js-logger.svg\n    :target: https://pypi.python.org/pypi/django-js-logger\n\n.. image:: https://codecov.io/gh/sondrelg/django-js-logger/branch/master/graph/badge.svg\n    :alt: Code coverage\n    :target: https://codecov.io/gh/sondrelg/django-js-logger/\n\n.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n    :alt: Pre-commit enabled\n    :target: https://github.com/pre-commit/pre-commit\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :alt: Code style black\n    :target: https://pypi.org/project/django-swagger-tester/\n\n.. image:: http://www.mypy-lang.org/static/mypy_badge.svg\n    :alt: Checked with mypy\n    :target: http://mypy-lang.org/\n\n|\n\nThis is a very simple Django app for forwarding console logs and console errors to dedicated Django loggers.\n\nUseful for catching Javascript errors that are not logged by Django natively and would otherwise only be logged to the client\'s console. Can be particularly useful if you have JavaScript running on top of our server-side rendered views.\n\nThe app works by posting *all relevant events* to an internal Django API, which logs them to one of two loggers. Not sure what impact this has on an apps performance, but it likely should not run anywhere near performance-sensitive production environments. Primarily this is intended to be a debugging aid.\n\nA flowchart of the app\'s structure looks something like this:\n\n.. image:: docs/img/flowchart.png\n\nThe package is open to contributions.\n\nInstallation\n------------\n\nInstalling with pip::\n\n    pip install django-js-logger\n\nInstalling with poetry::\n\n    poetry add django-js-logger\n\nQuick start\n-----------\n\n1. Add ``django_js_logger`` to your INSTALLED_APPS settings::\n\n    INSTALLED_APPS = [\n        ...\n        \'django_js_logger\',\n    ]\n\n2. Include the packages URLconf in your project urls.py like this::\n\n    path(\'js-logs/\', include(\'django_js_logger.urls\')),\n\n3. Optionally, specify your logging preferences by adding ``JS_LOGGER`` to your settings::\n\n    JS_LOGGER = {\n        \'CONSOLE_LOG_LEVEL\': \'INFO\',\n        \'CONSOLE_ERROR_LEVEL\': \'WARNING\'\n    }\n\n4. Add the required static file to your project by running ``manage.py collectstatic``. This should add a folder, ``django_js_logger`` with the file ``logger.js``. If this is not the case, you can copy the file manually from the demo project above.\n\n5. Import ``logger.js`` in the views you wish to log from by adding a JS import to your templates::\n\n    <script src="static/django_js_logger/logger.js"></script>\n',
    'author': 'Sondre Lillebø Gundersen',
    'author_email': 'sondrelg@live.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/snok/django-js-logger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
