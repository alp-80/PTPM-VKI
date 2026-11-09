import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lab1_code import register_user, _validate_login, _validate_password


class TestLoginValidation(unittest.TestCase):

    def test_valid_phone_login_accepted(self):
        ok, msg = _validate_login("+7-999-123-4567")
        self.assertTrue(ok)
        self.assertEqual(msg, "")

    def test_valid_email_login_accepted(self):
        ok, msg = _validate_login("use3r2@mail.ru")
        self.assertTrue(ok)
        self.assertEqual(msg, "")

    def test_valid_simple_login_accepted(self):
        ok, msg = _validate_login("vlad_popapov")
        self.assertTrue(ok)
        self.assertEqual(msg, "")

    def test_empty_login_rejected(self):
        ok, msg = _validate_login("")
        self.assertFalse(ok)
        self.assertEqual(msg, "Логин не может быть пустым")

    def test_short_login_string_rejected(self):
        ok, msg = _validate_login("ab")
        self.assertFalse(ok)
        self.assertIn("минимум 5", msg)

    def test_blacklisted_login_rejected(self):
        ok, msg = _validate_login("admin")
        self.assertFalse(ok)
        self.assertIn("чёрном списке", msg)


class TestPasswordValidation(unittest.TestCase):

    def test_valid_password_accepted(self):
        ok, msg = _validate_password("Пароль1!")
        self.assertTrue(ok)
        self.assertEqual(msg, "")

    def test_short_password_rejected(self):
        ok, msg = _validate_password("Па1!")
        self.assertFalse(ok)
        self.assertIn("минимум 7", msg)

    def test_password_with_latin_rejected(self):
        ok, msg = _validate_password("Passw0rd!")
        self.assertFalse(ok)
        self.assertIn("только кириллицу", msg)

    def test_password_without_special_char_rejected(self):
        ok, msg = _validate_password("Пароль11")
        self.assertFalse(ok)
        self.assertIn("спецсимвол", msg)


class TestRegisterUserIntegration(unittest.TestCase):

    def test_full_registration_success(self):
        ok, msg = register_user("vlad_popapov", "Пароль1!", "Пароль1!")
        self.assertTrue(ok)
        self.assertEqual(msg, "")

    def test_registration_with_mismatched_passwords(self):
        ok, msg = register_user("vlad_popapov", "Пароль1!", "Пароль2!")
        self.assertFalse(ok)
        self.assertIn("не совпадают", msg)

    def test_registration_returns_login_error_first(self):
        ok, msg = register_user("ab", "x", "x")
        self.assertFalse(ok)
        self.assertIn("минимум 5", msg)


if __name__ == "__main__":
    unittest.main()