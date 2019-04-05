import http
from typing import overload

from flask import jsonify

from flaskapp.abstractClasses import AbstractStructure
from flaskapp.models.base_model import BaseModel


def string_to_response(string):
    """
    Parse a string to an application/json
    :param string: The string to parse into json response.
    :return: The Json response.
    """
    return jsonify(string)


def bool_to_response(b: bool):
    """
    Parse a string to an application/json
    :param b: The boolean to parse into json response.
    :return: The Json response.
    """
    return jsonify(b)

@overload
def model_to_response(model: AbstractStructure):
    """
    Parse a model to an application/json
    :param model: Expected to be a child of AbstractStructure. The model to parse into json response.
    :return: The Json response.
    """

    return jsonify(model.to_dict())

@overload
def model_to_response(entities: [any]):
    """
    Parse a list of entities to an application/json
    :param entities: A list of model to parse into json response.
    :return: The Json response.
    """

    model_dict = [entity.to_dict() for entity in entities]

    return jsonify(model_dict)


def model_to_response(entities: BaseModel or [BaseModel]):
    """
    Parse a entity model or a list of it to an application/json
    :param entities: The model or a list of it to parse into json response.
    :return: The Json response.
    """

    if type(entities) == list:
        model_dict = [entity.to_dict() for entity in entities]
    else:
        model_dict = entities.to_dict()

    return jsonify(model_dict)


def empty_response():
    """
    Create a null response with the right http status.
    :return: The null response with http status: 204
    """
    return "", http.HTTPStatus.NO_CONTENT
