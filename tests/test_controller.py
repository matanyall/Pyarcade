from pyarcade.controller import Controller
import unittest


_USER1 = 'user1'
_PASSWORD = 'password'
# Set the password confirmation to match the password, by default.
_CONFIRM = _PASSWORD
_TYPO = 'f'


class ControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.controller = Controller()
        # Issue a SAVEPOINT so the database can be rolled back between tests.
        self.controller.begin_nested()

    def tearDown(self):
        # Roll back the database.
        self.controller.rollback()

    def test_sanitize(self):
        # TODO: implement sanitize.
        pass

    def test_register_success(self):
        status = self.controller.register(_USER1, _PASSWORD, _CONFIRM)
        self.assertTrue(status)

    def test_register_passwords_dont_match(self):
        confirm_typo = _PASSWORD + _TYPO

        status = self.controller.register(_USER1, _PASSWORD, confirm_typo)
        self.assertFalse(status)

    def test_register_username_already_taken(self):
        self.controller.register(_USER1, _PASSWORD, _CONFIRM)

        status = self.controller.register(_USER1, _PASSWORD, _CONFIRM)
        self.assertFalse(status)

    def test_get_user_by_username(self):
        self.controller.register(_USER1, _PASSWORD, _CONFIRM)

        user = self.controller._get_user(_USER1)
        self.assertTrue(user)
        self.assertEqual(user.username, _USER1)
        self.assertEqual(user.passwd, _PASSWORD)

    def test_get_user_by_username_and_password(self):
        self.controller.register(_USER1, _PASSWORD, _CONFIRM)

        user = self.controller._get_user(_USER1, _PASSWORD)
        self.assertTrue(user)
        self.assertEqual(user.username, _USER1)
        self.assertEqual(user.passwd, _PASSWORD)

    def test_get_user_by_username_not_found(self):
        user = self.controller._get_user(_USER1)
        self.assertFalse(user)

    def test_get_user_by_username_and_password_not_found(self):
        self.controller.register(_USER1, _PASSWORD, _CONFIRM)

        # Request an existing user, but with the wrong password.
        passwd_typo = _PASSWORD + _TYPO
        user = self.controller._get_user(_USER1, passwd_typo)
        self.assertFalse(user)

        # Request a nonexistant user, but with a password that another user is
        # using.
        nonexistant_user = _USER1 + _TYPO
        user = self.controller._get_user(nonexistant_user, _PASSWORD)
        self.assertFalse(user)

    def test_authenticate_success(self):
        self.controller.register(_USER1, _PASSWORD, _CONFIRM)

        status = self.controller.authenticate(_USER1, _PASSWORD)
        self.assertTrue(status)

    def test_authenticate_failure(self):
        # Do not worry about special cases, as they are tested in
        # test_get_user_* and authenticate is essentially a wrapper.
        status = self.controller.authenticate(_USER1, _PASSWORD)
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

        self.controller.register(u1, p1, p1)
        self.controller.register(u2, p2, p2)
        self.controller.register(u3, p3, p3)

        status = self.controller.authenticate(u2, p2)
        self.assertTrue(status)

        status = self.controller.authenticate(u3, p1)
        self.assertFalse(status)

