from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import CustomUser
from .validators import PasswordPolicyValidator
from .serializers import LoginSerializer, UserSerializer


class PasswordPolicyValidatorTests(TestCase):
    def setUp(self):
        self.validator = PasswordPolicyValidator()

    def test_valid_password_passes(self):
        self.validator.validate('ValidPass123!')

    def test_too_short_fails(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('Va1!')

    def test_no_uppercase_fails(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('validpass123!')

    def test_no_lowercase_fails(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('VALIDPASS123!')

    def test_no_digit_fails(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('ValidPass!!!')

    def test_no_special_char_fails(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('ValidPass123')

    def test_get_help_text(self):
        text = self.validator.get_help_text()
        self.assertIn('uppercase', text)
        self.assertIn('lowercase', text)


class CustomUserModelTests(TestCase):
    def test_create_user_defaults(self):
        user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='TestPass123!'
        )
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_locked)
        self.assertEqual(user.failed_login_attempts, 0)

    def test_create_superuser_is_staff(self):
        admin = CustomUser.objects.create_superuser(
            username='admin', email='admin@example.com', password='AdminPass123!'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_str_returns_email(self):
        user = CustomUser.objects.create_user(
            username='u1', email='u1@example.com', password='TestPass123!'
        )
        self.assertEqual(str(user), 'u1@example.com')

    def test_email_must_be_unique(self):
        CustomUser.objects.create_user(username='u1', email='dupe@example.com', password='TestPass123!')
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(username='u2', email='dupe@example.com', password='TestPass123!')


class LoginSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='TestPass123!'
        )

    def test_valid_credentials_return_user(self):
        s = LoginSerializer(data={'email': 'test@example.com', 'password': 'TestPass123!'})
        self.assertTrue(s.is_valid())
        self.assertEqual(s.validated_data['user'], self.user)

    def test_wrong_password_is_invalid(self):
        s = LoginSerializer(data={'email': 'test@example.com', 'password': 'WrongPass!'})
        self.assertFalse(s.is_valid())

    def test_unknown_email_is_invalid(self):
        s = LoginSerializer(data={'email': 'nobody@example.com', 'password': 'TestPass123!'})
        self.assertFalse(s.is_valid())

    def test_failed_attempt_increments_counter(self):
        LoginSerializer(data={'email': 'test@example.com', 'password': 'WrongPass!'}).is_valid()
        self.user.refresh_from_db()
        self.assertEqual(self.user.failed_login_attempts, 1)

    def test_three_failures_lock_account(self):
        for _ in range(3):
            LoginSerializer(data={'email': 'test@example.com', 'password': 'WrongPass!'}).is_valid()
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_locked)

    def test_locked_account_is_invalid(self):
        self.user.is_locked = True
        self.user.save()
        s = LoginSerializer(data={'email': 'test@example.com', 'password': 'TestPass123!'})
        self.assertFalse(s.is_valid())

    def test_successful_login_resets_failed_attempts(self):
        self.user.failed_login_attempts = 2
        self.user.save()
        LoginSerializer(data={'email': 'test@example.com', 'password': 'TestPass123!'}).is_valid()
        self.user.refresh_from_db()
        self.assertEqual(self.user.failed_login_attempts, 0)


class UserSerializerTests(TestCase):
    def test_includes_expected_fields(self):
        user = CustomUser.objects.create_user(
            username='u1', email='u1@example.com', password='TestPass123!',
            first_name='Alice', last_name='Smith'
        )
        data = UserSerializer(user).data
        self.assertEqual(data['email'], 'u1@example.com')
        self.assertEqual(data['first_name'], 'Alice')
        self.assertEqual(data['last_name'], 'Smith')

    def test_excludes_sensitive_fields(self):
        user = CustomUser.objects.create_user(
            username='u1', email='u1@example.com', password='TestPass123!'
        )
        data = UserSerializer(user).data
        self.assertNotIn('password', data)
        self.assertNotIn('failed_login_attempts', data)
