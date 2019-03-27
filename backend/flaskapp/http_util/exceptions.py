import http

from flask import jsonify

from flaskapp import app


# Exceptions Classes

class PermissionDenied(Exception):

    status_code = http.HTTPStatus.UNAUTHORIZED

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


# Register exceptions in the app.

@app.errorhandler(PermissionDenied)
def handle_permission_denied(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
