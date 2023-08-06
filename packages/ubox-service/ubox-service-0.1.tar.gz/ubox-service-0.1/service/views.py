from django.http import JsonResponse
from service.decorators import register, SERVICE_APP_NAME, SERVICE_APP_DESCRIBE, services, routes, SERVICE_APP_ID


@register('endpoint', ['/api/endpoint'], methods=['GET'], tags=['anonymous'], hans='服务信息')
def endpoint(request):
    """
    服务配置
    """
    data = {
        'id': SERVICE_APP_ID,
        'name': SERVICE_APP_NAME,
        'describe': SERVICE_APP_DESCRIBE,
        'config': {'services': services, 'routes': routes}
    }
    return JsonResponse(data=data)
