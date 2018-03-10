from sqlalchemy.exc import IntegrityError

from app.common.exceptions import DuplicateEntryException
from app.models import User
from base_dao import BaseDao


class UserDao(BaseDao):
    """Dao providing access to User model"""

    def __init__(self, db):
        self.db = db

    def insert(self, resource_data):
        """Insert a user record

        :param resource_data: user request payload data
        :raise DuplicateEntry exception if user already exists
        :return: User object
        """

        user = User(resource_data)
        self.db.session.add(user)
        try:
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            self.db.session.close()
            raise DuplicateEntryException

        return user

    def get(self, resource_id):
        """Get user by id

        :param resource_id: id of user
        :return: User object
        """
        return self.db.session.query(User).filter_by(id=resource_id).first()

    def get_by_email(self, email):
        """Get user by email

        :param email: email of user
        :return: User object
        """
        return self.db.session.query(User).filter_by(email=email).first()

    def update(self, user, data):
        """Update a user

        :param user: user to update
        :param data: new user data
        :return: update User object
        """
        for key, value in data.items():
            setattr(user, key, value)
        self.db.session.commit()
        return user
