import logging

import requests

from approve.models import Permission
from permission.settings import KONG_SERVICES_PATH, KONG_ROUTES_PATH, KONG_PERMISSION_OPR_MAP, KONG_AUTH_TAG, \
    KONG_PERMISSION_MAP, KONG_ROUTE_PATH, KONG_SERVICE_PATH, KONG_SERVICE_JWT_PATH, KONG_CONSUMERS_PATH, \
    KONG_ROUTE_ACL_PATH, KONG_SUPER_GROUP

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)


def install_services(services):
    """
    安装服务
    """
    for service in services:
        try:
            result = requests.post(KONG_SERVICES_PATH, data=service, timeout=8)
            if result.status_code == 201:
                logger.info('Service {} {}'.format(service.get('name'), 'create success.'))
                if KONG_AUTH_TAG in service.get('tags', []):
                    data = {
                        'name': 'jwt',
                        'config.claims_to_verify': 'exp'
                    }

                    result = requests.post(KONG_SERVICE_JWT_PATH.format(service.get('name')), data=data, timeout=8)
                    if result.status_code == 201:
                        logger.info('Service {} JWT {}'.format(service.get('name'), 'create success.'))
                    else:
                        logger.info('Service {} JWT {}'.format(service.get('name'), 'create failed.'))
            else:
                logger.warning('Service {} {}'.format(service.get('name'), 'create failed.'))
        except requests.exceptions.RequestException:
            logger.error('API gateway request failed')


def install_routes(routes):
    """
    安装路由
    """
    for route in routes:
        for method in route.get('methods', []):
            opr = KONG_PERMISSION_OPR_MAP.get(method)
            if opr is not None:
                data = route.copy()
                del data['hans']
                data['name'] = '{}_{}_{}'.format(opr, data.get('service'), data.get('name'))
                data['methods'] = [method, 'OPTIONS']
                data['protocols'] = ['http']
                data['strip_path'] = 'false'

                try:
                    result = requests.post(KONG_ROUTES_PATH.format(data.get('service')), data=data, timeout=8)

                    if result.status_code == 201:
                        if KONG_AUTH_TAG in data.get('tags', []):
                            action = KONG_PERMISSION_MAP.get(method)
                            p = Permission(id=data.get('name'), name='{}{}'.format(action, route.get('hans')))
                            p.save()

                        logger.info('Route {} {}'.format(data.get('name'), 'create success.'))

                        if KONG_AUTH_TAG in data.get('tags', []):
                            sync_acl(data.get('name'), [KONG_SUPER_GROUP])
                    else:
                        logger.warning('Route {} {}'.format(data.get('name'), 'create failed.'))
                except requests.exceptions.RequestException:
                    logger.error('API gateway request failed')


def uninstall_services(services):
    """
    卸载服务
    """
    for service in services:
        try:
            result = requests.delete(KONG_SERVICE_PATH.format(service.get('name')), timeout=8)
            if result.status_code == 204:
                logger.info('Service {} {}'.format(service.get('name'), 'delete success.'))
            else:
                logger.warning('Service {} {}'.format(service.get('name'), 'delete failed.'))
        except requests.exceptions.RequestException:
            logger.error('API gateway request failed')


def uninstall_routes(routes):
    """
    卸载路由
    """
    for route in routes:
        for method in route.get('methods', []):
            opr = KONG_PERMISSION_OPR_MAP.get(method)
            if opr is not None:
                name = '{}_{}_{}'.format(opr, route.get('service'), route.get('name'))

                try:
                    result = requests.delete(KONG_ROUTE_PATH.format(name), timeout=8)

                    if result.status_code == 204:
                        p = Permission.objects.filter(id=name)
                        p.delete()
                        logger.info('Route {} {}'.format(name, 'delete success.'))
                    else:
                        logger.warning('Route {} {}'.format(name, 'delete failed.'))
                except requests.exceptions.RequestException:
                    logger.error('API gateway request failed')


def create_user(username):
    """
    创建用户
    """
    try:
        result = requests.post(KONG_CONSUMERS_PATH, data='')
        if result.status_code == 201:
            logger.info('Consumers {} {}'.format(username, 'create success.'))
        else:
            logger.warning('Consumers {} {}'.format(username, 'create failed.'))
    except requests.exceptions.RequestException:
        logger.error('API gateway request failed')


def sync_acl(route, group):
    """
    同步用户组
    """
    try:
        data = {
            'name': 'acl',
            'config.whitelist': ','.join(group)
        }
        result = requests.post(KONG_ROUTE_ACL_PATH.format(route), data=data, timeout=8)
        if result.status_code == 201:
            logger.info('Route {} acls {} {}'.format(route, ','.join(group), 'create success.'))
        else:
            logger.warning('Route {} acls {} {}'.format(route, ','.join(group), 'create failed.'))
    except requests.exceptions.RequestException:
        logger.error('API gateway request failed')
