# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djarg', 'djarg.tests']

package_data = \
{'': ['*'], 'djarg.tests': ['templates/tests/*']}

install_requires = \
['django-formtools>=2.2,<3.0', 'django>=2', 'python-args>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'django-args',
    'version': '1.1.0',
    'description': 'Django wrappers for python-args functions.',
    'long_description': 'django-args\n###########\n\n``django-args`` is the `Django <https://www.djangoproject.com/>`__\nwrapper on `python-args <https://github.com/jyveapp/python-args>`__.\n\n``python-args`` provides the ability to decorate functions with validators,\ncontext, and default value processors. ``django-args`` takes this a\nstep further, allowing any function decorated with ``python-args`` to\nseamlessly integrate with Django form views and form wizards.\n\nFor example, ``djarg.views.FormView`` automatically constructs a Django\n``FormView`` on a python function and maps the form fields to the\nfunction arguments. Assuming the function is wrapped with\n``arg.validators``, ``django-args`` will seamlessly bind\nthe validators to the form. This same concept is extended to bulk\nviews and form views offered by ``django-args``.\n\nAlong with this, ``django-args`` also helps eliminate the burden\nof passing around variables from views to forms for doing simple\ninitializations (choice fields, etc) and other boilerplate that\ncan become difficult to follow as a project grows.\n\nCheck out the `docs <https://django-args.readthedocs.io/>`__ for\nmore information on how you can use ``django-args`` for your\nproject. \n\nDocumentation\n=============\n\n`View the django-args docs here\n<https://django-args.readthedocs.io/>`_.\n\nInstallation\n============\n\nInstall django-args with::\n\n    pip3 install django-args\n\nAfter this, add ``djarg`` to the ``INSTALLED_APPS``\nsetting of your Django project.\n\nContributing Guide\n==================\n\nFor information on setting up django-args for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\nPrimary Authors\n===============\n\n- @wesleykendall (Wes Kendall)\n',
    'author': 'Wes Kendall',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyveapp/django-args',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
