from app import db
from app.daos import UserDao, TokenDao
from app.models import User, Token
from tests.test_base import BaseTestCase


class TokenDaoTests(BaseTestCase):
    """A class for token dao tests"""

    def setUp(self):
        super(TokenDaoTests, self).setUp()

        self.mock_user_data = self.load_fixtures("users_fixtures/default_user.yaml")
        self.mock_user_response = self.load_fixtures("users_fixtures/user_response.yaml")

        self.user = User(self.mock_user_data)
        self.token = Token(self.user)
        db.session.commit()
        db.session.add(self.user)
        db.session.commit()

        self.user_dao = UserDao(db)
        self.token_dao = TokenDao(db)

    def test_insert_token(self):
        """Ensure token is inserted"""

        token = self.token_dao.insert_user_token(self.user)
        user = self.user_dao.get(self.user.id)

        self.assertIn(token, user.tokens)

    def test_generate_token(self):
        """Ensure token is generated"""

        token = self.token_dao.insert_user_token(self.user)

        self.assertTrue(len(token.generate_auth_token()) == 166)

    def test_verify_token(self):
        """Ensure token is verified"""

        token = self.token_dao.insert_user_token(self.user)
        user = Token.verify_auth_token(token.generate_auth_token())

        expected_user = self.mock_user_response
        expected_user['id'] = self.user.id

        self.assertEqual(user.to_json(), expected_user)

    def test_invalid_token(self):
        """Ensure token is invalid"""

        token = self.token_dao.insert_user_token(self.user)
        user = Token.verify_auth_token("fake token")

        expected_user = self.mock_user_response
        expected_user['id'] = self.user.id

        self.assertIsNone(user)

    def test_get_token(self):
        """Ensure token is present"""

        token = self.token_dao.insert_user_token(self.user)
        token_gen = token.generate_auth_token()
        valid_token = Token.get_auth_token(token_gen)

        self.assertEqual(valid_token.to_json(), token.to_json())

    def test_expire_token(self):
        """Ensure token is expired"""

        invalid_token = Token.get_auth_token("some token")

        self.assertIsNone(invalid_token)
