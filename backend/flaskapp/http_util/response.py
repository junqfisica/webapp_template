import http

from flask import jsonify

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


def model_to_response(entities: BaseModel or [BaseModel]):
    """
    Parse a entity or a list of entities to an application/json
    :param entities: The model to parse into json response.
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
