from flask import abort
from flask_login import current_user
from functools import wraps
from jobweb.models import User, Job_detail, Company

def role_required(role):
    def decorator(func) :
        @wraps(func)
        def wrapper(*args, **kwrargs):
            if not current_user.is_authenticated or current_user.role < role:
                abort(404)
            return func(*args, **kwrargs)
        return wrapper
    return decorator

#company_required = role.required(User.COMPANY)
admin_required = role_required(User.ADMIN)

