import uuid

from sqlalchemy import Column, String
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    pw_hash = Column(String(200), nullable=False)

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
