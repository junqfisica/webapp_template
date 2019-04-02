from datetime import datetime

from flaskapp import db
from flaskapp.models import BaseModel, TableNames


class RoleModel(db.Model, BaseModel):

    # The name of the table at the data base.
    __tablename__ = TableNames.S_ROLES

    # The table columns.
    role_id = db.Column(db.String(50), primary_key=True)
    label = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return "Role(role_id={})".format(self.role_id)

    @classmethod
    def is_valid_role(cls, role_id: str):
        role = cls.find_by_id(role_id)
        if role:
            return True

        return False


class UserRoleModel(db.Model, BaseModel):

    # The name of the table at the data base.
    __tablename__ = TableNames.T_USER_ROLES

    # The table columns.
    user_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_USER + ".id"), primary_key=True)
    role_id = db.Column(db.String(50), db.ForeignKey(TableNames.S_ROLES + ".role_id"), primary_key=True)
    lastchange_by = db.Column(db.String(16), unique=False, nullable=True)
    lastchange_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "UserRole(id={}, role={})".format(self.user_id, self.role_id)
