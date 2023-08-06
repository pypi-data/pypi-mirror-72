# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgtrigger', 'pgtrigger.tests', 'pgtrigger.tests.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2']

setup_kwargs = {
    'name': 'django-pgtrigger',
    'version': '1.0.1',
    'description': 'Postgres trigger support integrated with Django models.',
    'long_description': "django-pgtrigger\n################\n\n``django-pgtrigger`` provides primitives for configuring\n`Postgres triggers <https://www.postgresql.org/docs/current/sql-createtrigger.html>`__\non Django models.\n\nModels can be decorated with `pgtrigger.register` and supplied with\n`pgtrigger.Trigger` objects. These will automatically be installed after\nmigrations. Users can use Django idioms such as ``Q`` and ``F`` objects to\ndeclare trigger conditions, alleviating the need to write raw SQL for a large\namount of use cases.\n\n``django-pgtrigger`` comes built with some derived triggers for expressing\ncommon patterns. For example, ``pgtrigger.Protect`` can protect operations\non a model, such as deletions or updates (e.g. an append-only model). The\n``pgtrigger.Protect`` trigger can even target protecting operations on\nspecific updates of fields (e.g. don't allow updates if ``is_active`` is\n``False`` on a model). Another derived trigger, ``pgtrigger.SoftDelete``,\ncan soft-delete models by setting a field to ``False`` when a deletion\nhappens on the model.\n\nRead the `pgtrigger docs <https://django-pgtrigger.readthedocs.io/>`__ for\nexamples of how to use triggers in your application.\n\n\nDocumentation\n=============\n\n`View the django-pgtrigger docs here\n<https://django-pgtrigger.readthedocs.io/>`_.\n\nInstallation\n============\n\nInstall django-pgtrigger with::\n\n    pip3 install django-pgtrigger\n\nAfter this, add ``pgtrigger`` to the ``INSTALLED_APPS``\nsetting of your Django project.\n\nContributing Guide\n==================\n\nFor information on setting up django-pgtrigger for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\nPrimary Authors\n===============\n\n- @wesleykendall (Wes Kendall)\n",
    'author': 'Wes Kendall',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyveapp/django-pgtrigger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
