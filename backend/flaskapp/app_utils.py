from functools import wraps

from flask import jsonify

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
        @app.route(api_url_prefix + url_path)
        def wrap_func(*args, **kwargs):
            return func(*args, **kwargs)
        return wrap_func
    return app_decorator


def parse_to_json_response(obj):
    """
    Parse a string to a application/json
    :param obj: The model to parse into json response.
    :return: The Json response.
    """
    return jsonify(obj)
