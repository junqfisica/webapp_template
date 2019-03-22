from datetime import datetime

from flask_bcrypt import Bcrypt

from flaskapp import db
from flaskapp.models.base_model import BaseModel


class RelationShip:
    USER_ROLE = "UserRoleModel"
    USER = "UserModel"
    ROLE = "RoleModel"


class UserModel(db.Model, BaseModel):

    # The name of the table at the data base.
    __tablename__ = "t_user"

    # The table columns.
    user_id = db.Column(db.String(16), primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.relationship(RelationShip.USER_ROLE, backref="user", lazy=True)

    def __repr__(self):
        return "User({})".format(self.username)

    def to_dict(self):
        """
        Convert UserModel into a dictionary, this way we can convert it to a JSON response.
        :return: A clean dictionary form of this model.
        """
        # convert columns to dict
        dict_representation = super().to_dict()

        # add role
        role = "None"
        # A user can have only one role.
        if len(self.role) == 1:
            role = self.role[0].role_id

        dict_representation["role"] = role

        return dict_representation

    def has_valid_password(self, password):
        bcrypt = Bcrypt()
        return bcrypt.check_password_hash(self.password, password)

    # Queries for this model.
    @classmethod
    def find_by_username(cls, username):
        # user = cls.query.filter_by(username=username).first()
        user = cls.find_by(username=username)
        if user:
            return user

        return None


class RoleModel(db.Model, BaseModel):

    # The name of the table at the data base.
    __tablename__ = "s_roles"

    # The table columns.
    role_id = db.Column(db.String(50), primary_key=True)
    label = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return "Role(role_id={})".format(self.role_id)


class UserRoleModel(db.Model, BaseModel):

    # The name of the table at the data base.
    __tablename__ = "t_user_roles"

    # The table columns.
    user_id = db.Column(db.String(16), db.ForeignKey(UserModel.__tablename__+".user_id"), primary_key=True)
    role_id = db.Column(db.String(50), db.ForeignKey(RoleModel.__tablename__+".role_id"), primary_key=True)
    lastchange_by = db.Column(db.String(16), unique=False, nullable=True)
    lastchange_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "UserRole(user_id={}, role={})".format(self.user_id, self.role_id)
