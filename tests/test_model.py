from pyarcade.model import Model
import unittest


_USER1 = 'user1'
_PASSWORD = 'password'
# Set the password confirmation to match the password, by default.
_CONFIRM = _PASSWORD
_TYPO = 'f'


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.model = Model()
        # Issue a SAVEPOINT so the database can be rolled back between tests.
        self.model.begin_nested()

    def tearDown(self):
        # Roll back the database.
        self.model.rollback()

    def test_sanitize(self):
        # TODO: implement sanitize.
        pass

    def test_add_user_success(self):
        status = self.model.add_user(_USER1, _PASSWORD, _CONFIRM)
        self.assertTrue(status)

    def test_add_user_passwords_dont_match(self):
        confirm_typo = _PASSWORD + _TYPO

        status = self.model.add_user(_USER1, _PASSWORD, confirm_typo)
        self.assertFalse(status)

    def test_add_user_username_already_taken(self):
        self.model.add_user(_USER1, _PASSWORD, _CONFIRM)

        status = self.model.add_user(_USER1, _PASSWORD, _CONFIRM)
        self.assertFalse(status)

    def test_get_user_by_username(self):
        self.model.add_user(_USER1, _PASSWORD, _CONFIRM)

        user = self.model._get_user(_USER1)
        self.assertTrue(user)
        self.assertEqual(user.username, _USER1)
        self.assertEqual(user.passwd, _PASSWORD)

    def test_get_user_by_username_and_password(self):
        self.model.add_user(_USER1, _PASSWORD, _CONFIRM)

        user = self.model._get_user(_USER1, _PASSWORD)
        self.assertTrue(user)
        self.assertEqual(user.username, _USER1)
        self.assertEqual(user.passwd, _PASSWORD)

    def test_get_user_by_username_not_found(self):
        user = self.model._get_user(_USER1)
        self.assertFalse(user)

    def test_get_user_by_username_and_password_not_found(self):
        self.model.add_user(_USER1, _PASSWORD, _CONFIRM)

        # Request an existing user, but with the wrong password.
        passwd_typo = _PASSWORD + _TYPO
        user = self.model._get_user(_USER1, passwd_typo)
        self.assertFalse(user)

        # Request a nonexistant user, but with a password that another user is
        # using.
        nonexistant_user = _USER1 + _TYPO
        user = self.model._get_user(nonexistant_user, _PASSWORD)
        self.assertFalse(user)

    def test_authenticate_user_success(self):
        self.model.add_user(_USER1, _PASSWORD, _CONFIRM)

        status = self.model.authenticate_user(_USER1, _PASSWORD)
        self.assertTrue(status)

    def test_authenticate_user_failure(self):
        # Do not worry about special cases, as they are tested in
        # test_get_user_* and authenticate_user is essentially a wrapper.
        status = self.model.authenticate_user(_USER1, _PASSWORD)
        self.assertFalse(status)

    def test_stress_1(self):
        # Perform several registrations/insertions, followed by many
        # authentications/lookups.
        u1 = _USER1
        u2 = 'user2'
        u3 = 'bob'
        p1 = _PASSWORD
        p2 = _PASSWORD
        p3 = '1234'

        self.model.add_user(u1, p1, p1)
        self.model.add_user(u2, p2, p2)
        self.model.add_user(u3, p3, p3)

        status = self.model.authenticate_user(u2, p2)
        self.assertTrue(status)

        status = self.model.authenticate_user(u3, p1)
        self.assertFalse(status)

