from sqlalchemy import Column
from sqlalchemy.exc import SQLAlchemyError

from flaskapp import db, app_logger


class BaseModel:

    def __init__(self, *args, **kwargs):
        super(BaseModel).__init__(self, *args, **kwargs)

    def to_dict(self):
        """
        Transforms the entity columns into a dictionary. This is equivalent to a Dto.

        Import: This method only converts the Columns fields. For tables with
        relationship, you must extend this method and add the relationships as desired.

        :return: A dictionary representation of the entity's columns.
        """

        # Check if is the right instance.
        if isinstance(self, db.Model):
            # construct a dictionary from column names and values.
            dict_representation = {c.name: getattr(self, c.name) for c in self.__table__.columns}
            return dict_representation
        else:
            raise AttributeError(type(self).__name__ + " is not instance of " + db.Model.__name__)

    @classmethod
    def from_dict(cls, dto):
        """
        Gets a Model from a dictionary representation of it. Usually a Dto.
        :param dto: The data transfer object as a dictionary.
        :return: The model represent this class.
        """
        # Map column names back to dto fields. The keys must be equal to the column name.
        clean_dict = {c.name: dto[c.name] for c in cls.__table__.columns}
        return cls(**clean_dict)

    def save(self):
        """
        Insert or Update the given entity.
        :return: True if succeed, false otherwise.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except SQLAlchemyError as error_message:
            app_logger.error(error_message)
            return False

    def delete(self):
        """
        Delete the given entity.
        :return: True if succeed, false otherwise.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as error_message:
            app_logger.error(error_message)
            return False

    @classmethod
    def __class_validation(cls):
        """
        Used to validate the class.
        :return:
        """

        # check if this class is a subClass of Model
        if not issubclass(cls, db.Model):
            raise AttributeError(cls.__name__ + " is not subclass of " + db.Model.__name__)

    @classmethod
    def find_by_id(cls, entity_id):
        """
        Find by id.
        :param entity_id: The id of the entity.
        :return: The entity if found, None otherwise.
        """

        # Validate class before query
        cls.__class_validation()

        entity = cls.query.get(entity_id)
        if entity:
            return entity

        return None

    @classmethod
    def get_all(cls, order_by: Column = None):
        """
        Get all entities from this model.
        @:param order_by: (Optional) The Column to sort the query.
        :return: The list of entities, None otherwise.
        """
        # Validate class before query
        cls.__class_validation()

        if order_by:
            entity_list = cls.query.order_by(order_by).all()
        else:
            entity_list = cls.query.all()

        if entity_list:
            return entity_list

        return None

    @classmethod
    def find_by(cls, get_first: bool = True, **kwarg):
        """
        Find by an specific column name.

        :param get_first: (default=True). If True return one value, otherwise it will try to get
        all entries that match the query.
        :param kwarg: The column name as key and the value to match, e.g username="Jon". If more than one
            filter is given the query will use AND to join it.
            Important: you must pass at least one kwarg to this method, otherwise a ValueError will raise.
        :return: The entity if is_unique=True and it exists or a list of entity if is_unique=False and exists.
            None, otherwise.
        """
        # Validate class before query
        cls.__class_validation()

        if len([*kwarg]) < 1:
            raise ValueError("find_by must have at least one **kwarg")

        if get_first:
            entity = cls.query.filter_by(**kwarg).first()
        else:
            entity = cls.query.filter_by(**kwarg).all()

        if entity:
            return entity

        return None
