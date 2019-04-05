from typing import NamedTuple

from flaskapp.abstractClasses import AbstractStructure


class UserSearch(AbstractStructure, NamedTuple):

    Page: int
    PerPage: int
    OrderBy: str

    @classmethod
    def __validate_dictionary(cls, dic):
        """
         Force the dictionary to have the same type of the parameter's declaration.
        :param dic: The dictionary to be validate.
        :return: A new dictionary that try to keeps the same data type from this class parameters.
        """
        valid_dic = {}
        for k in dic.keys():
            if cls._field_types.get(k) == int:
                valid_dic[k] = int(dic.get(k))
            elif cls._field_types.get(k) == float:
                valid_dic[k] = float(dic.get(k))
            elif cls._field_types.get(k) == str:
                valid_dic[k] = str(dic.get(k))
            else:
                valid_dic[k] = dic.get(k)
        return valid_dic

    def to_dict(self):
        return self._asdict()

    @classmethod
    def from_dict(cls, dictionary):
        new_d = cls.__validate_dictionary(dictionary)
        return cls(**new_d)


class SearchResult(AbstractStructure, NamedTuple):
    result: any
    total: int

    def to_dict(self):
        return self._asdict()

    @classmethod
    def from_dict(cls, dictionary):
        return cls(**dictionary)
