from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


def current_user_exists(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user and current_user.is_authenticated:
            return redirect(url_for('frontend.index'))
        return f(*args, **kwargs)

    return wrapper
