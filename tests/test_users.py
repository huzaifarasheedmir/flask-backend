import unittest
import json

from flask import url_for

from app import create_app, db
from app.models import User


class TestUser(unittest.TestCase):
    """A class for user tests"""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.headers = {'Content-Type': 'application/json'}
        self.user = User({"name": "abc", "email": "abcd@xyz.com", "password": "12345678"})
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_201(self):
        """Ensure user is registered"""

        body = json.dumps({"name": "abc", "email": "abc@xyz.com", "password": "12345678"})

        response = self.client.post(url_for('users.register_user'),
                                    data=body,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 201)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEquals(response_json, {"name": "abc", "email": "abc@xyz.com", "id": response_json['id']})

    def test_register_409(self):
        """Ensure user already exists"""

        body = json.dumps({"name": "abc", "email": "abcd@xyz.com", "password": "12345678"})

        response = self.client.post(url_for('users.register_user'),
                                    data=body,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 409)

    def test_register_400(self):
        """Ensure user register payload is invalid"""

        body = json.dumps({"name": 2, "email": "abcd@xyz.com"})

        response = self.client.post(url_for('users.register_user'),
                                    data=body,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 400)

    def test_login_200(self):
        """Ensure user is authorized"""

        body = json.dumps({"email": "abcd@xyz.com", "password": "12345678"})

        response = self.client.post(url_for('users.login_user'),
                                    data=body,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_login_401(self):
        """Ensure user is unauthorized"""

        body = json.dumps({"email": "abcd@xyz.com", "password": "invalid"})

        response = self.client.post(url_for('users.login_user'),
                                    data=body,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 401)

    def test_login_404(self):
        """Ensure user to login not exists"""

        body = json.dumps({"email": "abcde@xyz.com", "password": "invalid"})

        response = self.client.post(url_for('users.login_user'),
                                    data=body,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_login_400(self):
        """Ensure user to login payload is invalid"""

        body = json.dumps({"email": "abcde@xyz.com", "abc": "invalid"})

        response = self.client.post(url_for('users.login_user'),
                                    data=body,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_get_200(self):
        """Ensure a user exists"""

        response = self.client.get(url_for('users.get_user', user_id=self.user.id),
                                   headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEquals(json.loads(response.data.decode('utf-8')), self.user.to_json())

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
        self.assertEquals(json.loads(response.data.decode('utf-8')), self.user.to_json())

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
