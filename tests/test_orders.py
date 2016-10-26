import json

from flask import url_for

from tests.base import BaseTestCase


class TestOrder(BaseTestCase):
    """A class for order tests"""

    def test_post_201(self):
        """Ensure an order is placed."""

        body = json.dumps({"name": "abc", "amount": 3})

        response = self.client.post(url_for('orders.place_order'),
                                    data=body,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 201)
        self.assertEquals(json.loads(response.data.decode('utf-8')), {"name": "abc", "amount": 3, "id": "123456789"})

    def test_get_200(self):
        """Ensure an order exists"""

        response = self.client.get(url_for('orders.get_order', id="123456789"),
                                   headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEquals(json.loads(response.data.decode('utf-8')), {"name": "abc", "amount": 3, "id": "123456789"})

    def test_get_404(self):
        """Ensure an order doesnt exist"""

        response = self.client.get(url_for('orders.get_order', id="invalid"),
                                   headers=self.headers)

        self.assertEqual(response.status_code, 404)

    def test_patch_200(self):
        """Ensure an order is updated"""

        body = json.dumps({"amount": 6})

        response = self.client.patch(url_for('orders.update_order', id="123456789"),
                                     data=body,
                                     headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEquals(json.loads(response.data.decode('utf-8')), {"name": "abc", "amount": 6, "id": "123456789"})

    def test_patch_404(self):
        """Ensure an order doesnt exist to update"""

        body = json.dumps({"amount": 6})

        response = self.client.patch(url_for('orders.update_order', id="invalid"),
                                     data=body,
                                     headers=self.headers)

        self.assertEqual(response.status_code, 404)

    def test_delete_204(self):
        """Ensure an order is deleted"""

        response = self.client.delete(url_for('orders.delete_order', id="123456789"),
                                      headers=self.headers)

        self.assertEqual(response.status_code, 204)

    def test_delete_404(self):
        """Ensure an order doesnt exist to deleted"""

        response = self.client.delete(url_for('orders.delete_order', id="invalid"),
                                      headers=self.headers)

        self.assertEqual(response.status_code, 404)
