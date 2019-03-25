from flaskapp import app_logger
from flaskapp.app_utils import path, query_param
from flaskapp.models.user_model import UserModel
from flaskapp.http_util import response


@path("/login")
@query_param("username", "password")
def login(username, password):
    user = UserModel.find_by_username(username)
    if user and user.has_valid_password(password):
        # print("User login successfully.")
        app_logger.info("User login successfully.")
        return response.model_to_response(user)
    else:
        app_logger.warning("Fail to login.")
        return response.empty_response()
