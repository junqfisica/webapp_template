# User APIs.
from flask_login import current_user

from flaskapp.api import users
from flaskapp.http_util import response as response
from flaskapp.http_util.decorators import secure, post, query
from flaskapp.http_util.exceptions import UserNotFound
from flaskapp.models import UserModel, Role, RoleModel
from flaskapp.search.structures import UserSearch, SearchResult


def __is_username_taken(username: str) -> bool:
    user = UserModel.find_by_username(username)
    if user:
        return True
    return False


@users.route("/<string:user_id>", methods=["GET"])
def get_user(user_id: str):
    user = UserModel.find_by_id(user_id)
    if user:
        return response.model_to_response(user)

    return response.empty_response()


@users.route("/roles", methods=["GET"])
def get_roles():
    roles = RoleModel.get_all(order_by=RoleModel.label)
    if roles:
        return response.model_to_response(roles)

    return response.empty_response()


@users.route("/all", methods=["GET"])
@secure(Role.ADMIN)
def get_users():

    all_users = UserModel.get_all()

    if all_users:
        return response.model_to_response(all_users)

    return response.empty_response()


@users.route("/search", methods=["GET"])
@secure(Role.ADMIN)
@query(UserSearch)
def search(user_search: UserSearch):

    user_list = UserModel.pagination(per_page=user_search.PerPage, page=user_search.Page)
    model_dict = [entity.to_dict() for entity in user_list]
    total = UserModel.total()
    if users:
        return response.model_to_response(SearchResult(result=model_dict, total=total))
    return response.empty_response()


@users.route("/username/<string:username>", methods=["GET"])
def get_user_by_username(username: str):
    user = UserModel.find_by_username(username)

    if user:
        return response.model_to_response(user)

    return response.empty_response()


@users.route("/isTaken/<string:username>", methods=["GET"])
def is_taken(username: str):
    user_exist = __is_username_taken(username)
    return response.bool_to_response(user_exist)


@users.route("/create", methods=["POST"])
@secure(Role.ADMIN)
@post()
def create_user(user: dict):
    # create a user model from user data.
    user_model = UserModel.create_user(user, current_user.id)

    # Check if user with the same username don't exist.
    if __is_username_taken(user_model.username):
        return response.bool_to_response(False)

    created = user_model.save()

    return response.bool_to_response(created)


@users.route("/delete/<string:user_id>", methods=["DELETE"])
@secure(Role.ADMIN)
def delete_user(user_id):
    print(user_id)
    user = UserModel.find_by_id(user_id)
    if not user:
        raise UserNotFound("The user id {} doesn't exist".format(user_id))

    deleted = user.delete()
    return response.bool_to_response(deleted)
