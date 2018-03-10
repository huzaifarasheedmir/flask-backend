from app import db
from app.common.exceptions import DuplicateEntryException
from app.daos import UserDao
from app.models import User
from tests.test_base import BaseTestCase


class CaseUserDaoTests(BaseTestCase):
    """A class for user dao tests"""

    def setUp(self):
        super(CaseUserDaoTests, self).setUp()

        self.mock_user_data = self.load_fixtures("users_fixtures/default_user.yaml")
        self.mock_user_response = self.load_fixtures("users_fixtures/user_response.yaml")

        self.user = User(self.mock_user_data)
        db.session.add(self.user)
        db.session.commit()
        self.user_dao = UserDao(db)

    def test_insert_user(self):
        """Ensure user is inserted"""

        new_user_data = self.mock_user_data
        new_user_data['email'] = "abcde@xyz.com"
        user = self.user_dao.insert(new_user_data)

        expected_user = self.mock_user_response
        expected_user['id'] = user.id
        expected_user['email'] = "abcde@xyz.com"

        self.assertEqual(user.to_json(), expected_user)

    def test_duplicate_user(self):
        """Ensure user already exists"""

        with self.assertRaises(DuplicateEntryException):
            self.user_dao.insert(self.mock_user_data)

    def test_get_user(self):
        """Ensure user is fetched by id"""

        expected_user = self.mock_user_response
        expected_user['id'] = self.user.id
        user = self.user_dao.get(self.user.id)

        self.assertEqual(user.to_json(), expected_user)

    def test_get_user_not_exists(self):
        """Ensure user doesnt exist"""

        user = self.user_dao.get("123")

        self.assertIsNone(user)

    def test_get_user_by_email(self):
        """Ensure user is fetched by email"""

        expected_user = self.mock_user_response
        expected_user['id'] = self.user.id
        user = self.user_dao.get_by_email(self.user.email)

        self.assertEqual(user.to_json(), expected_user)

    def test_get_user_not_exists_by_email(self):
        """Ensure user doesnt exist by email"""

        user = self.user_dao.get_by_email("some@email.com")

        self.assertIsNone(user)

    def test_update_user(self):
        """Ensure user is updated"""

        expected_user = self.mock_user_response
        expected_user['name'] = 'abc'
        expected_user['id'] = self.user.id
        user = self.user_dao.update(self.user, {"name": "abc"})

        self.assertEqual(user.to_json(), expected_user)

    def test_update_user_not_exists(self):
        """Ensure user update fails if user not exists"""

        new_user_data = self.mock_user_data
        new_user_data['email'] = "abcdefg@xyz.com"
        user = User(new_user_data)
        user1 = self.user_dao.update(user, {"name": "abcd"})
        user2 = self.user_dao.get(user1.id)

        self.assertIsNone(user2)
