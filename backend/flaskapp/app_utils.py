from functools import wraps

from flaskapp import app
from flaskapp.api import api_url_prefix


def path(url_path=""):
    """
    Append the api url prefix in the app.router().
    :param url_path: The api url, e.g /getuser/ or /getuser/<int:id>
    :return: The decorated function
    """
    def app_decorator(func):
        @wraps(func)
        @app.route(api_url_prefix + url_path, endpoint=func.__name__)
        def wrap_func(*args, **kwargs):
            return func(*args, **kwargs)
        return wrap_func
    return app_decorator
