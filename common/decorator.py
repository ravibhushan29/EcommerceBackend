from functools import wraps
from rest_framework.exceptions import NotAuthenticated


def required_role(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.user.role_type in roles:
                return func(request, *args, **kwargs)
            else:
                raise NotAuthenticated("Not allow to access")
        return wrapper
    return decorator