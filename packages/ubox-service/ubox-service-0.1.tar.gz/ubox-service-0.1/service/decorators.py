from django.conf import settings

METHODS_LIST = ['GET', 'POST', 'PUT', 'DELETE']
TAGS_LIST = ['authentication', 'anonymous']

SERVICE_APP_ID = getattr(settings, 'SERVICE_APP_ID', None)
SERVICE_APP_NAME = getattr(settings, 'SERVICE_APP_NAME', None)
SERVICE_APP_DESCRIBE = getattr(settings, 'SERVICE_APP_DESCRIBE', None)

SERVICE_API_PROTOCOL = getattr(settings, 'SERVICE_API_PROTOCOL', ['http'])
SERVICE_API_IP = getattr(settings, 'SERVICE_API_IP', None)
SERVICE_API_PORT = getattr(settings, 'SERVICE_API_PORT', 80)

SERVICE_DEFAULT_SERVICE = getattr(settings, 'SERVICE_DEFAULT_SERVICE', None)
SERVICE_DEFAULT_METHODS = getattr(settings, 'SERVICE_DEFAULT_METHODS', ['GET', 'POST', 'PUT', 'DELETE'])
SERVICE_DEFAULT_TAGS = getattr(settings, 'SERVICE_DEFAULT_TAGS', ['authentication'])

services = [
    {
        'name': SERVICE_DEFAULT_SERVICE,
        'protocol': SERVICE_API_PROTOCOL,
        'host': SERVICE_API_IP,
        'port': SERVICE_API_PORT,
        'path': '/',
        'tags': SERVICE_DEFAULT_TAGS
    }
]

routes = []


def register(name, paths, methods=None, service=None, tags=None, hans=None):
    """
    """
    def wrapper(clazz):
        if isinstance(name, str) is not True:
            raise ValueError('The name is not a string.')

        if isinstance(paths, list) is not True:
            raise ValueError('The paths is not a list.')

        if methods is not None and set(methods).issubset(set(METHODS_LIST)) is not True:
            raise ValueError('The methods is not legal.')

        if tags is not None and set(tags).issubset(set(TAGS_LIST)) is not True:
            raise ValueError('The tags is not legal.')

        if service is not None and isinstance(service, str) is not True:
            raise ValueError('The service is not a string.')

        if hans is not None and isinstance(hans, str) is not True:
            raise ValueError('The hans is not a string.')

        if service is not None:
            if service not in [s.get('name') for s in services]:
                s = {
                    'name': service,
                    'protocol': SERVICE_API_PROTOCOL,
                    'host': SERVICE_API_IP,
                    'port': SERVICE_API_PORT,
                    'path': '/',
                    'tags': ['authentication']
                }

                if tags is not None:
                    s['tags'] = tags

                services.append(s)

        route = {
            'name': name,
            'methods': methods or SERVICE_DEFAULT_METHODS,
            'tags': tags or SERVICE_DEFAULT_TAGS,
            'paths': paths,
            'service': service or SERVICE_DEFAULT_SERVICE,
            'hans': hans or name
        }
        routes.append(route)

        return clazz
    return wrapper
