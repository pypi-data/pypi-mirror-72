=============
Ubox Service
=============

Service is a Django app. For each question,

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "service" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'service.apps.ServiceConfig',
    ]

2. Include the service URLconf in your project urls.py like this::

    path('/api/endpoint', include('service.urls')),


3. Visit http://127.0.0.1:8000//api/endpoint.