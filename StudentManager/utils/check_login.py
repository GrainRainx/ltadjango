from django.shortcuts import redirect
from django.conf import settings


def check_login(func):  # 自定义登录验证装饰器
    def warpper(request, *args, **kwargs):
        is_login = request.session.get('is_login', False)
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect(settings.LOGIN_URL)

    return warpper
