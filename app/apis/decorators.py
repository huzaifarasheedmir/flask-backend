"""
Validations and authentication decorators for all APIs
"""

from flask import abort, request
from functools import wraps
from jsonschema import validate, ValidationError


def validate_schema(schema):
    """Validate request payload
    :param schema: dict containing the payload definition
    :type schema: dict

    :return 400 Response if payload is invalid
    """

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            data = request.get_json(force=True)
            if not data:
                abort(400)
            try:
                validate(data, schema)
            except ValidationError:
                abort(400)
            return func(*args, **kwargs)

        return decorated_function

    return decorator
