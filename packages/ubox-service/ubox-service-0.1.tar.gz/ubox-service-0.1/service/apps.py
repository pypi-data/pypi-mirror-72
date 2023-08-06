from django.apps import AppConfig

from service.decorators import SERVICE_APP_NAME, SERVICE_APP_DESCRIBE, SERVICE_API_IP, SERVICE_DEFAULT_SERVICE, \
    SERVICE_DEFAULT_METHODS, SERVICE_APP_ID


class ServiceConfig(AppConfig):
    name = 'service'

    def ready(self):
        """
        在子类中重写此方法，以便在Django启动时运行代码。
        """
        # 启动时检查环境变量是否设置
        if SERVICE_APP_ID is None:
            raise ValueError('Settings SERVICE_APP_ID unconfigured.')

        if SERVICE_APP_NAME is None:
            raise ValueError('Settings SERVICE_APP_NAME unconfigured.')

        if SERVICE_APP_DESCRIBE is None:
            raise ValueError('Settings SERVICE_APP_DESCRIBE unconfigured.')

        if SERVICE_API_IP is None:
            raise ValueError('Settings SERVICE_API_IP unconfigured.')

        if SERVICE_DEFAULT_SERVICE is None:
            raise ValueError('Settings SERVICE_DEFAULT_SERVICE unconfigured.')

        if SERVICE_DEFAULT_METHODS is None:
            raise ValueError('Settings SERVICE_DEFAULT_METHODS unconfigured.')
