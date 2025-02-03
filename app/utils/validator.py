from functools import update_wrapper
from flask import jsonify, request, make_response
from cerberus import Validator


def errorValidation(errors):
    response = {
        "response": 400,
        "message": "Bad request was sent",
        "errors": errors
    }

    result = jsonify(response)
    result.status_code = response["response"]

    return result


def validate(schema):
    def decorator(f):
        def wrapped_function(*args, **kws):
            valid_params = _validate(schema)

            if not valid_params == True:
                return valid_params

            return f(*args, **kws)
        return update_wrapper(wrapped_function, f)
    return decorator


def _validate(schema):
    params = request.get_json(silent=True) or request.form.to_dict()

    v = Validator(schema)
    result = v(params)

    if not result:
        errors = v.errors
        error = errorValidation(errors)
        return make_response(error)

    return True
