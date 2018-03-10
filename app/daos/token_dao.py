from app.models import Token
from base_dao import BaseDao


class TokenDao(BaseDao):
    """Dao providing access to Token model"""

    def __init__(self, db):
        self.db = db

    def insert_user_token(self, user):
        """Insert oauthToken against a user

        :param user: user object
        :return: generated token object
        """
        token = Token(user.id)
        self.db.session.add(token)
        self.db.session.commit()
        return token
