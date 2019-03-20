# user api.

from flaskapp.app_utils import path, parse_to_json_response


@path("/users/<int:user_id>")
def get_user(user_id):
    user = {"name": "Thiago", "id": user_id}
    return parse_to_json_response(user)
