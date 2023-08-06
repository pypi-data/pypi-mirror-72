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

    path('api/', include(service.urls)),

3. Add the following configuration to settings::

    # Name and description of the application
    SERVICE_APP_ID = 'test'
    SERVICE_APP_NAME = 'Testing service'
    SERVICE_APP_DESCRIBE = 'Testing service for reference only.'

    # The protocol, address, and port of the service
    SERVICE_API_PROTOCOL = ['http']
    SERVICE_API_IP = '192.168.X.X'
    SERVICE_API_PORT = '80'

    # Default service name, request method
    SERVICE_DEFAULT_SERVICE = 'test'
    SERVICE_DEFAULT_METHODS = ['GET', 'POST', 'PUT', 'DELETE']

4. Add register decorator to an API class view or function::

    @register('demo', ['/api/demo'], methods=['GET'], hans='demo')
    def demo(request):
        return ''

5. Visit http://127.0.0.1:8000/api/endpoint.