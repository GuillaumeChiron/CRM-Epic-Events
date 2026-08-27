from functools import wraps


def roles_required(*roles):

    def decorator(func):

        @wraps(func)
        def wrapper(self, current_user, *args, **kwargs):

            if current_user.role.name not in roles:
                return False

            return func(self, current_user, *args, **kwargs)

        return wrapper

    return decorator


gestion_required = roles_required("gestion")
commercial_required = roles_required("commercial")
support_required = roles_required("support")


def owner_required(get_owner_id, *bypass_roles):

    def decorator(func):

        @wraps(func)
        def wrapper(self, current_user, *args, **kwargs):

            if current_user.role.name in bypass_roles:
                return func(self, current_user, *args, **kwargs)

            if get_owner_id(*args, **kwargs) != current_user.id:
                return False

            return func(self, current_user, *args, **kwargs)

        return wrapper

    return decorator
