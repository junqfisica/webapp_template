import sys
import traceback
from typing import NamedTuple

from flaskapp import app_logger
from flaskapp.abstractClasses import AbstractStructure
from flaskapp.http_util.exceptions import AppException


class Search(AbstractStructure, NamedTuple):

    SearchBy: str
    SearchValue: str
    Page: int
    PerPage: int
    OrderBy: str
    OrderDesc: bool

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
            elif cls._field_types.get(k) == bool:
                valid_dic[k] = True if dic.get(k).capitalize() == "True" else False
            elif cls._field_types.get(k) == str:
                if dic.get(k) == "null":
                    valid_dic[k] = None
                else:
                    valid_dic[k] = str(dic.get(k))
            else:
                valid_dic[k] = dic.get(k)
        return valid_dic

    def to_dict(self):
        return self._asdict()

    @classmethod
    def from_dict(cls, dictionary):
        new_d = cls.__validate_dictionary(dictionary)
        try:
            return cls(**new_d)

        except TypeError as error:
            traceback.print_exc(limit=2, file=sys.stdout)
            app_logger.error(traceback.format_exc())
            raise AppException(str(error))


class SearchResult(AbstractStructure, NamedTuple):
    result: any
    total: int

    def to_dict(self):
        return self._asdict()

    @classmethod
    def from_dict(cls, dictionary):
        try:
            return cls(**dictionary)

        except TypeError as error:
            traceback.print_exc(limit=2, file=sys.stdout)
            app_logger.error(traceback.format_exc())
            raise AppException(str(error))
