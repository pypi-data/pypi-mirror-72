Django EasyAudit Utils
======================

This is a simple Django app to provide hand views, analytics and tools for better handling data from easyaudit_.


Detailed documentation is in the "docs" directory.

Quick start
-----------
1. Install the package using::

    pip install django-easyaudit-utils

2. Add "easyaudit_utils" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'easyaudit',
        'easyaudit_utils',
        ...
    ]

3. Include the polls URLconf in your project urls.py like this::

    path("easyaudit/", include("easyaudit_utils.urls", namespace="easyaudit_utils")),


.. _easyaudit: https://github.com/soynatan/django-easy-audit

