import http

from flask import jsonify

from flaskapp.models.base_model import BaseModel


def string_to_response(obj):
    """
    Parse a string to an application/json
    :param obj: The model to parse into json response.
    :return: The Json response.
    """
    return jsonify(obj)


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
