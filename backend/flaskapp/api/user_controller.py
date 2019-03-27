# User APIs.

from flaskapp.api import users
from flaskapp.http_util import response as response
from flaskapp.http_util.decorators import secure
from flaskapp.models import UserModel, Role


@users.route("/<string:user_id>", methods=["GET"])
def get_user(user_id):
    user = UserModel.find_by_id(user_id)
    if user:
        return response.model_to_response(user)

    return response.empty_response()


@users.route("/all", methods=["GET"])
@secure(Role.ADMIN)
def get_users():

    all_users = UserModel.get_all()

    if all_users:
        return response.model_to_response(all_users)

    return response.empty_response()


@users.route("/username/<string:username>", methods=["GET"])
def get_user_by_username(username):
    user = UserModel.find_by_username(username)

    if user:
        return response.model_to_response(user)

    return response.empty_response()
