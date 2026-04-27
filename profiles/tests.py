from django.test import TestCase
from accounts.models import CustomUser
from profiles.models import EmployeeProfile
from profiles.serializers import PublicProfileSerializer, PrivateProfileSerializer


class ProfileSignalTests(TestCase):
    def test_profile_auto_created_on_user_creation(self):
        user = CustomUser.objects.create_user(
            username='u1', email='u1@example.com', password='TestPass123!'
        )
        self.assertTrue(EmployeeProfile.objects.filter(user=user).exists())

    def test_profile_not_duplicated_on_user_save(self):
        user = CustomUser.objects.create_user(
            username='u1', email='u1@example.com', password='TestPass123!'
        )
        user.first_name = 'Updated'
        user.save()
        self.assertEqual(EmployeeProfile.objects.filter(user=user).count(), 1)


class PublicProfileSerializerTests(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(
            username='u1', email='u1@example.com', password='TestPass123!'
        )
        self.profile = EmployeeProfile.objects.get(user=user)
        self.profile.job_role = 'Engineer'
        self.profile.salary = '50000.00'
        self.profile.save()

    def test_includes_public_fields(self):
        data = PublicProfileSerializer(self.profile).data
        self.assertIn('job_role', data)
        self.assertIn('department', data)
        self.assertIn('about_me', data)

    def test_excludes_private_fields(self):
        data = PublicProfileSerializer(self.profile).data
        self.assertNotIn('salary', data)
        self.assertNotIn('phone_number', data)
        self.assertNotIn('address', data)
        self.assertNotIn('date_of_birth', data)


class PrivateProfileSerializerTests(TestCase):
    def setUp(self):
        self.manager = CustomUser.objects.create_user(
            username='mgr', email='mgr@example.com', password='TestPass123!',
            first_name='Bob', last_name='Jones'
        )
        user = CustomUser.objects.create_user(
            username='u1', email='u1@example.com', password='TestPass123!'
        )
        self.profile = EmployeeProfile.objects.get(user=user)
        self.profile.salary = '45000.00'
        self.profile.save()

    def test_includes_private_fields(self):
        data = PrivateProfileSerializer(self.profile).data
        self.assertIn('salary', data)
        self.assertIn('phone_number', data)
        self.assertIn('address', data)

    def test_line_manager_name_with_full_name(self):
        self.profile.line_manager = self.manager
        self.profile.save()
        data = PrivateProfileSerializer(self.profile).data
        self.assertEqual(data['line_manager_name'], 'Bob Jones')

    def test_line_manager_name_falls_back_to_email(self):
        nameless = CustomUser.objects.create_user(
            username='mgr2', email='mgr2@example.com', password='TestPass123!'
        )
        self.profile.line_manager = nameless
        self.profile.save()
        data = PrivateProfileSerializer(self.profile).data
        self.assertEqual(data['line_manager_name'], 'mgr2@example.com')

    def test_line_manager_name_is_none_when_unset(self):
        data = PrivateProfileSerializer(self.profile).data
        self.assertIsNone(data['line_manager_name'])
