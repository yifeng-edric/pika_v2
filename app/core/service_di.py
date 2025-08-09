from app.services.factory import ServiceFactory, PlatformType


def get_service_adapter(platform_type: PlatformType):
    return ServiceFactory.get_service(platform_type.value)
