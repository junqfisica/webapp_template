from functools import wraps

from flask import request

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


def query_param(*params):
    def app_decorator(func):
        @wraps(func)
        def wrap_func(*args, **kwargs):
            request_values = (request.args.get(param) for param in params)
            args = request_values
            return func(*args, **kwargs)
        return wrap_func
    return app_decorator

