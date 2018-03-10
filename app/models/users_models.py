import uuid
from datetime import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from config import config


class User(db.Model):
    __tablename__ = 'users'
    id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    pw_hash = Column(String(200), nullable=False)
    tokens = relationship('Token', backref='user', cascade="all, delete-orphan", lazy='dynamic')

    def __init__(self, data):
        self.id = str(uuid.uuid4())
        self.name = data['name']
        self.email = data['email']
        self.set_password(data['password'])

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def to_json(self):
        json_user = {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
        return json_user


class Token(db.Model):
    __tablename__ = 'tokens'
    id = Column(String(50), primary_key=True)
    issued_at = Column(DateTime, nullable=False)
    user_id = Column(String(50), ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id):
        self.id = str(uuid.uuid4().hex)
        self.user_id = user_id
        self.issued_at = datetime.utcnow()

    def to_json(self):
        return {
            "id": self.id,
            "issued_at": self.issued_at.isoformat()
        }

    def generate_auth_token(self, expiration=604800):
        s = Serializer(config['default'].SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(config['default'].SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token

        token = Token.query.get(data['id'])
        if not token:
            return None

        return token.user

    @staticmethod
    def get_auth_token(token):
        s = Serializer(config['default'].SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token

        token = Token.query.get(data['id'])
        if not token:
            return None

        return token
