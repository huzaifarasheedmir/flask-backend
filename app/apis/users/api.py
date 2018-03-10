"""
All users APIs users are placed here
"""

from flask import current_app, request, Response, jsonify

from app import db
from app.apis.decorators import validate_schema
from app.apis.users import users
from app.common.exceptions import DuplicateEntryException
from app.daos import UserDao, TokenDao
from consts import INVALID_CREDENTIALS, USER_ALREADY_EXISTS, USER_REGISTERED, UPDATED_USER, USER_NOT_FOUND
from schema import register_user, login_user, update_user

user_dao = UserDao(db)
token_dao = TokenDao(db)


@users.route('/register', methods=['POST'])
@validate_schema(register_user)
def register_user():
    """Create a user

    :return 201 Response if user registrations is successful
    :return 409 Response if a user with provided email is already registered
    """

    data = request.get_json(force=True)

    try:
        user = user_dao.insert(data)
        current_app.logger.info(USER_REGISTERED.format(user.email))
        resp = jsonify(user.to_json())
        resp.status_code = 201
        return resp

    except DuplicateEntryException:
        current_app.logger.error(USER_ALREADY_EXISTS.format(data['email']))
        return Response(status=409)


@users.route('/login', methods=['POST'])
@validate_schema(login_user)
def login_user():
    """Login a user

    :return 404 Response if user doesnt exists
    :return 401 Response if password is wrong
    :return 200 with user data response containing auth token after a successful login
    """

    data = request.get_json(force=True)

    user = user_dao.get_by_email(email=data['email'])
    if not user:
        current_app.logger.error(USER_NOT_FOUND.format(data['email']))
        return Response(status=404)

    if not user.check_password(data['password']):
        current_app.logger.error(INVALID_CREDENTIALS.format(user.email))
        return Response(status=401)

    token = token_dao.insert_user_token(user)
    response_data = user.to_json()
    response_data['token'] = token.generate_auth_token()

    resp = jsonify(response_data)
    resp.status_code = 200
    return resp


@users.route('/<user_id>', methods=['PATCH'])
@validate_schema(update_user)
def update_user(user_id):
    """Update a user

    :param user_id: id assigned to user after registration
    :type user_id:str
    :return 404 Response if user doesnt exists
    :return 200 with updated user data response
    """

    data = request.get_json(force=True)

    user = user_dao.get(resource_id=user_id)
    if not user:
        current_app.logger.error(USER_NOT_FOUND.format(user_id))
        return Response(status=404)

    new_user = user_dao.update(user, data)
    current_app.logger.info(UPDATED_USER.format(user.email))
    resp = jsonify(new_user.to_json())
    resp.status_code = 200
    return resp


@users.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a user

    :param user_id: id assigned to user after registration
    :type user_id: int
    :return 404 Response if user doesnt exists
    :return 200 with user data response
    """

    user = user_dao.get(resource_id=user_id)
    if not user:
        current_app.logger.error(USER_NOT_FOUND.format(user_id))
        return Response(status=404)

    resp = jsonify(user.to_json())
    resp.status_code = 200
    return resp
