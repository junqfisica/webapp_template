from flask import Blueprint

api_url_prefix = ""
# api_url_prefix = "/api"


api = Blueprint('api', __name__)
users = Blueprint('users', __name__)

from flaskapp.api import user_controller, login_controller
