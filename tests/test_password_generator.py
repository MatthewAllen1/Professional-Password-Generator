import string
import unittest
from unittest.mock import patch

from PasswordGenerator import generate_password


class PasswordGenerationTests(unittest.TestCase):
    def test_length_and_categories(self):
        password = generate_password(32, True, True, True, True)
        self.assertEqual(len(password), 32)
        self.assertTrue(any(c in string.ascii_uppercase for c in password))
        self.assertTrue(any(c in string.ascii_lowercase for c in password))
        self.assertTrue(any(c in string.digits for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))

    def test_single_category(self):
        password = generate_password(12, False, False, True, False)
        self.assertEqual(len(password), 12)
        self.assertTrue(all(c in string.digits for c in password))

    def test_invalid_length(self):
        for length in (0, -1, 11, 129, True, 3.5):
            with self.subTest(length=length):
                with self.assertRaises(ValueError):
                    generate_password(length, True, True, True, True)

    def test_no_categories(self):
        with self.assertRaises(ValueError):
            generate_password(20, False, False, False, False)

    def test_uses_secrets(self):
        with patch("PasswordGenerator.secrets.choice", return_value="A") as choice:
            result = generate_password(12, True, False, False, False)
        self.assertEqual(result, "A" * 12)
        self.assertTrue(choice.called)


if __name__ == "__main__":
    unittest.main()
