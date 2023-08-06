# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arg', 'arg.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-args',
    'version': '1.0.1',
    'description': 'Python argument design patterns in a composable interface.',
    'long_description': 'python-args\n############\n\npython-args, inspired by `attrs <https://www.attrs.org/en/stable/>`__,\nremoves the boilerplate of processing arguments to functions and methods.\n\nDecorating your functions with python-args decorators like ``arg.validators``\ncan make your code more composable, more readable, and easier to test. Along\nwith this, functions decorated with python-args can be used to by other tools\nand frameworks to build more expressive interfaces. The\n`django-args <https://github.com/jyveapp/django-args>`__ and\n`django-action-framework <https://github.com/jyveapp/django-action-framework>`__\nlibraries are two examples.\n\nThe core ``python-args`` decorators are as follows:\n\n1. ``@arg.validators(*validation_funcs)``: Runs validation functions that\n   can take the same named arguments as the decorated function. When\n   decorating a function with `arg.validators`, you not only de-couple\n   your function from argument validation logic, but ``python-args``\n   will allow other interfaces to only run the validators of your function.\n2. ``@arg.defaults(**arg_default_funcs)``: Sets arguments to default\n   values. The default functions can similarly take the same named\n   parameters of the decorated function.\n3. ``@arg.parametrize(**parametrize_funcs)``: Runs a function multiple times\n   for a particular input.\n4. ``@arg.contexts(*context_funcs)``: Enters context managers before\n   a function. Context managers can take the same named parameters as the\n   decorated function.\n\n`View the docs here <https://python-args.readthedocs.io/>`__\nfor a tutorial and more examples of how ``python-args`` can be used in\npractice.\n\nDocumentation\n=============\n\n`View the python-args docs here <https://python-args.readthedocs.io/>`_.\n\nInstallation\n============\n\nInstall python-args with::\n\n    pip3 install python-args\n\n\nContributing Guide\n==================\n\nFor information on setting up python-args for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\nPrimary Authors\n===============\n\n- @wesleykendall (Wes Kendall)\n',
    'author': 'Wes Kendall',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyveapp/python-args',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
