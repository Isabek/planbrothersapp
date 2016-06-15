from functools import wraps

from flask import redirect, url_for, request
from flask_login import current_user


def redirect_url(default='frontend.index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


def current_user_exists(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user and current_user.is_authenticated:
            return redirect(url_for('frontend.index'))
        return f(*args, **kwargs)

    return wrapper
