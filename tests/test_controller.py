from pyarcade.controller import Controller
import unittest


class ControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.controller = Controller()
        self.username = 'user1'
        self.passwd = 'password'
        # Set the password confirmation to match the password, by default.
        self.confirm = self.passwd
        self.__TYPO = 'f'

    def test_sanitize(self):
        # TODO: implement sanitize.
        pass

    def test_register_success(self):
        status = self.controller.register(self.username, self.passwd,
                self.confirm)
        self.assertTrue(status)

    def test_register_passwords_dont_match(self):
        confirm_typo = self.passwd + self.__TYPO

        status = self.controller.register(self.username, self.passwd,
                confirm_typo)
        self.assertFalse(status)

    def test_register_username_already_taken(self):
        self.controller.register(self.username, self.passwd, self.confirm)

        status = self.controller.register(self.username, self.passwd,
                self.confirm)
        self.assertFalse(status)

    def test_get_user_by_username(self):
        self.controller.register(self.username, self.passwd, self.confirm)

        user = self.controller.get_user(self.username)
        self.assertTrue(user)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.passwd, self.passwd)

    def test_get_user_by_username_and_password(self):
        self.controller.register(self.username, self.passwd, self.confirm)

        user = self.controller.get_user(self.username, self.passwd)
        self.assertTrue(user)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.passwd, self.passwd)

    def test_get_user_by_username_not_found(self):
        user = self.controller.get_user(self.username)
        self.assertFalse(user)

    def test_get_user_by_username_and_password_not_found(self):
        self.controller.register(self.username, self.passwd, self.confirm)

        # Request an existing user, but with the wrong password.
        passwd_typo = self.passwd + self.__TYPO
        user = self.controller.get_user(self.username, passwd_typo)
        self.assertFalse(user)

        # Request a nonexistant user, but with a password that another user is
        # using.
        nonexistant_user = self.user + self.__TYPO
        user = self.controller.get_user(nonexistant_user, self.passwd)
        self.assertFalse(user)

    def test_authenticate_success(self):
        self.controller.register(self.username, self.passwd, self.confirm)

        status = self.controller.authenticate(self.username, self.passwd)
        self.assertTrue(status)

    def test_authenticate_failure(self):
        # Do not worry about special cases, as they are tested in
        # test_get_user_* and authenticate is essentially a wrapper.
        status = self.controller.authenticate(self.username, self.passwd)
        self.assertFalse(status)

    def test_stress_1(self):
        # Perform several registrations/insertions, followed by many
        # authentications/lookups.
        u1 = self.username
        u2 = 'user2'
        u3 = 'bob'
        p1 = self.passwd
        p2 = self.passwd
        p3 = '1234'

        self.controller.register(u1, p1, p1)
        self.controller.register(u2, p2, p2)
        self.controller.register(u3, p3, p3)

        status = self.controller.authenticate(u2, p2)
        self.assertTrue(status)

        status = self.controller.authenticate(u3, p1)
        self.assertFalse(status)

