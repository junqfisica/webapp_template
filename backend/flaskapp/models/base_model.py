from flaskapp import db


class BaseModel:

    def to_dict(self):
        """
        The representation of the entity User. This is equivalent to a Dto.
        Import: For simple table models you can safaly use this. However, for tables with
        relationship overwrite this method to get what you expect.

        :return: A clean dictionary of this entity.
        """

        # Check if is the right instance.
        if isinstance(self, db.Model):
            # contruct a dictionary from column names and values.
            dict_representation = {c.name: getattr(self, c.name) for c in self.__table__.columns}
            return dict_representation
        else:
            raise AttributeError(type(self).__name__ + " is not instance of " + db.Model.__name__)

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
    def get_all(cls):
        """
        Get all entities from this model.
        :return: The list of entities, None otherwise.
        """
        # Validate class before query
        cls.__class_validation()

        entity_list = cls.query.all()
        if entity_list:
            return entity_list

        return None

    @classmethod
    def find_by(cls, is_unique: bool = True, **kwarg):
        """
        Find by an specific column name.

        :param is_unique: (default=True). If True return one value, otherwise it will try to get
        all entries that match the query.
        :param kwarg: The column name as key and the value to match, e.g username="Jon".
            Important: you must pass only one kwarg to this method, otherwise a ValueError will raise.
        :return: The entity if is_unique=True and it exists or a list of entity if is_unique=False and exists.
            None, otherwise.
        """
        # Validate class before query
        cls.__class_validation()

        if len([*kwarg]) != 1:
            raise ValueError("find_by must have only one **kwarg")

        if is_unique:
            entity = cls.query.filter_by(**kwarg).first()
        else:
            entity = cls.query.filter_by(**kwarg).all()

        if entity:
            return entity

        return None
