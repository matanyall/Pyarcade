from pyarcade.api import app, db
import unittest
import json


class BasicTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = db
        self.db.drop_all()
        self.db.create_all()

    def test_empty_response(self):
        response = self.app.get('/users')
        users = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(users), 0)

    def test_can_create_user(self):
        response = self.app.post(
            '/users',
            data=json.dumps({"username": "newuser", "password": "userpass"}),
            content_type='application/json'
        )
        user = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("newuser", user["username"])

    def test_can_delete_user(self):
        # create the user
        response = self.app.post(
            '/users',
            data=json.dumps({"username": "newuser", "password": "userpass"}),
            content_type='application/json'
        )

        # Get the user ID
        response = self.app.get(
            "/users",
            data=json.dumps(json.loads(response.data)),
            content_type='application/json'
        )

        # Try to delete
        users = json.loads(response.data)
        self.app.delete(
            "/users/{}".format(users[0]["id"]),
            content_type='application/json'
        )

        # Verify the user is gone by trying to get that particular user ID
        response = self.app.get(
            "/users/{}".format(users[0]["id"]),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
