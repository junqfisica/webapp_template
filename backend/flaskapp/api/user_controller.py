# User APIs.

from flaskapp.app_utils import path
from flaskapp.http_util import response as response
from flaskapp.models.user_model import UserModel


@path("/user/<string:user_id>")
def get_user(user_id):
    user = UserModel.find_by_id(user_id)
    if user:
        return response.parse_model_to_json_response(user)

    return response.empty_response()


@path("/users")
def get_users():

    users = UserModel.get_all()

    if users:
        return response.parse_model_to_json_response(users)

    return response.empty_response()


@path("/user/username/<string:username>")
def get_user_by_username(username):
    user = UserModel.find_by_username(username)

    if user:
        return response.parse_model_to_json_response(user)

    return response.empty_response()
