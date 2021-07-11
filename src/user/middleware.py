from django.conf import settings
from django.contrib.auth import logout
from datetime import datetime, timedelta


def timing_logout(get_response):
    """
    Разлогинивает пользователя спустя LOGOUT_TIMEOUT после последнего входа
    """
    ttl = settings.LOGOUT_TIMEOUT

    def middleware(request):
        user = request.user

        if not user.is_anonymous and user.last_login < datetime.now() - timedelta(seconds=ttl):
            logout(request)

        response = get_response(request)
        return response

    return middleware
