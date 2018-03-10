import json

from flask import url_for

from app import db
from app.models import User
from tests.test_base import BaseTestCase


class UserApisTests(BaseTestCase):
    """A class for user APIs tests"""

    def setUp(self):
        super(UserApisTests, self).setUp()

        db.create_all()
        self.client = self.app.test_client()

        self.headers = {'Content-Type': 'application/json'}
        self.mock_user_data = self.load_fixtures("users_fixtures/default_user.yaml")
        self.mock_user_response = self.load_fixtures("users_fixtures/user_response.yaml")

        self.user = User(self.mock_user_data)
        db.session.add(self.user)
        db.session.commit()

    def test_register_201(self):
        """Ensure user is registered"""

        payload = self.mock_user_data
        payload['email'] = "abc@xyz.com"
        body = json.dumps(payload)

        response = self.client.post(url_for('users.register_user'),
                                    data=body,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 201)

        response_json = json.loads(response.data.decode('utf-8'))
        expected_response = self.mock_user_response
        expected_response['id'] = response_json['id']
        expected_response['email'] = "abc@xyz.com"

        self.assertEquals(response_json, expected_response)

    def test_register_409(self):
        """Ensure user already exists"""

        body = json.dumps(self.mock_user_data)

        response = self.client.post(url_for('users.register_user'),
                                    data=body,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 409)

    def test_register_400(self):
        """Ensure user register payload is invalid"""

        payload = self.mock_user_data
        del payload['name']
        body = json.dumps(payload)

        response = self.client.post(url_for('users.register_user'),
                                    data=body,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 400)

    def test_login_200(self):
        """Ensure user is authorized"""

        payload = self.mock_user_data
        del payload['name']
        body = json.dumps(payload)

        response = self.client.post(url_for('users.login_user'),
                                    data=body,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data.decode('utf-8'))
        expected_response = self.mock_user_response
        expected_response['id'] = response_json['id']
        expected_response['token'] = response_json['token']

        self.assertEquals(response_json, expected_response)

    def test_login_401(self):
        """Ensure user is unauthorized"""

        payload = self.mock_user_data
        payload['password'] = "invalid"
        del payload['name']

        body = json.dumps(payload)

        response = self.client.post(url_for('users.login_user'),
                                    data=body,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 401)

    def test_login_404(self):
        """Ensure user to login not exists"""

        payload = self.mock_user_data
        payload['email'] = "abcde@xyz.com"
        del payload['name']
        body = json.dumps(payload)

        response = self.client.post(url_for('users.login_user'),
                                    data=body,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 404)

    def test_login_400(self):
        """Ensure user to login payload is invalid"""

        body = json.dumps(self.mock_user_data)

        response = self.client.post(url_for('users.login_user'),
                                    data=body,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 400)

    def test_get_200(self):
        """Ensure a user exists"""

        response = self.client.get(url_for('users.get_user', user_id=self.user.id),
                                   headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode('utf-8')), self.user.to_json())

    def test_get_user_404(self):
        """Ensure a user doesnt exist"""

        response = self.client.get(url_for('users.get_user', user_id="invalid"),
                                   headers=self.headers)

        self.assertEqual(response.status_code, 404)

    def test_update_200(self):
        """Ensure a user is updated"""

        body = json.dumps({"name": "test_name"})

        response = self.client.patch(url_for('users.update_user', user_id=self.user.id),
                                     data=body,
                                     headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode('utf-8')), self.user.to_json())

    def test_update_404(self):
        """Ensure a user to update doesnt exist"""

        body = json.dumps({"name": "test_name"})

        response = self.client.patch(url_for('users.update_user', user_id="invalid"),
                                     data=body,
                                     headers=self.headers)

        self.assertEqual(response.status_code, 404)

    def test_update_400(self):
        """Ensure a user to update payload is invalid"""

        body = json.dumps({"abc": "test_name"})

        response = self.client.patch(url_for('users.update_user', user_id=self.user.id),
                                     data=body,
                                     headers=self.headers)

        self.assertEqual(response.status_code, 400)
