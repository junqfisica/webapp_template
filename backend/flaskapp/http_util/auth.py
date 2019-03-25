from flaskapp import login_manager
from flaskapp.models.user_model import UserModel


@login_manager.user_loader
def load_user(user_id):
    return UserModel.find_by_id(user_id)
