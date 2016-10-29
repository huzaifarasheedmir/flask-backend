from app import db

from flask import request, Response, jsonify
from sqlalchemy.exc import IntegrityError

from app.models import User
from app.users import users


@users.route('/register', methods=['POST'])
def register_user():
    """Create a user"""

    data = request.get_json(force=True)

    user = User(data)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        db.session.close()
        return Response(status=409)

    resp = jsonify(user.to_json())
    resp.status_code = 201
    return resp


@users.route('/login', methods=['POST'])
def login_user():
    """Login a user"""

    data = request.get_json(force=True)

    user = db.session.query(User).filter_by(email=data['email']).first()
    if not user:
        return Response(status=404)

    if not user.check_password(data['password']):
        return Response(status=401)

    resp = jsonify(user.to_json())
    resp.status_code = 200
    return resp


@users.route('/<user_id>', methods=['PATCH'])
def update_user(user_id):
    """Update a user"""

    data = request.get_json(force=True)

    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return Response(status=404)

    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    resp = jsonify(user.to_json())
    resp.status_code = 200
    return resp


@users.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a user"""

    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return Response(status=404)

    resp = jsonify(user.to_json())
    resp.status_code = 200
    return resp

