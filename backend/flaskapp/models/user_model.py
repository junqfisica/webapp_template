from builtins import classmethod

from flask_login import UserMixin

from flaskapp import db, bcrypt, login_manager, app_logger, app_utils
from flaskapp.http_util import exceptions
from flaskapp.models import RelationShip, TableNames, TokenModel, UserRoleModel, RoleModel
from flaskapp.models.base_model import BaseModel


class UserModel(db.Model, BaseModel, UserMixin):

    # The name of the table at the data base.
    __tablename__ = TableNames.T_USER

    # The table columns.
    id = db.Column(db.String(16), primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    roles = db.relationship(RelationShip.USER_ROLE, backref="user", lazy=True)
    token = db.relationship(RelationShip.TOKEN, backref="user", lazy=True)

    def __repr__(self):
        return "User(id={}, username={})".format(self.id, self.username)

    @property
    def get_roles(self):
        """ Get a list of roles for this user."""
        return [role.role_id for role in self.roles if role]

    @property
    def get_token(self):
        """Get user token if any, otherwise returns None."""
        token_model = TokenModel.find_by_user_id(self.id)
        return token_model.token if token_model else None

    def to_dict(self):
        """
        Convert UserModel into a dictionary, this way we can convert it to a JSON response.
        :return: A clean dictionary form of this model.
        """
        # convert columns to dict
        dict_representation = super().to_dict()

        # add roles
        dict_representation["roles"] = self.get_roles
        # add token
        dict_representation["token"] = self.get_token

        return dict_representation

    def has_valid_password(self, password):
        """
        Verify if user has a valid password.
        :param password: The paswword to be verify.
        :return: True if password is valid, False otherwise.
        """
        return bcrypt.check_password_hash(self.password, password)

    def has_role(self, role):
        if role in self.get_roles:
            return True
        else:
            return False

    def add_roles(self, roles_ids: [str], current_user_id=None):

        for role_id in roles_ids:
            if RoleModel.is_valid_role(role_id):
                user_role = UserRoleModel(user_id=self.id, role_id=role_id, lastchange_by=current_user_id)
                self.roles.append(user_role)

    @classmethod
    def create_user(cls, user_dict, current_user_id=None):
        user = cls.from_dict(user_dict)
        user.id = app_utils.generate_id(16)
        user.password = app_utils.encrypt_password(user.password)

        # Add role relational field.
        roles_id = user_dict.get("roles")
        if not roles_id:
            raise exceptions.RoleNotFound("User must have at least one role assigned.")
        user.add_roles(roles_ids=roles_id, current_user_id=current_user_id)

        return user

    # Queries for this model.
    @classmethod
    def find_by_username(cls, username):
        user = cls.find_by(username=username)
        if user:
            return user

        return None


# Called when security is required or current_user.
@login_manager.request_loader
def load_user(request):
    # X-Access-Token come from the client side.
    # This header is add to requests at the token.interceptor at the Angular side.
    token = request.headers.get('X-Access-Token')
    if token:
        token_model = TokenModel.find_by(token=token)
        if token_model:
            return token_model.user  # This is possible because of backref = user.
        else:
            app_logger.warning("The toke {} don't exist in the database.".format(token))
            return None

    app_logger.warning("Header request don't have a token.")
    return None
