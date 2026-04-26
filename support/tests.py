from django.test import TestCase
from accounts.models import CustomUser
from support.models import SupportTicket
from support.serializers import SupportTicketSerializer


class SupportTicketModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='u1', email='u1@example.com', password='TestPass123!'
        )

    def test_default_status_is_open(self):
        ticket = SupportTicket.objects.create(
            submitted_by=self.user, subject='Test', category='it', description='Details'
        )
        self.assertEqual(ticket.status, 'open')

    def test_default_priority_is_medium(self):
        ticket = SupportTicket.objects.create(
            submitted_by=self.user, subject='Test', category='it', description='Details'
        )
        self.assertEqual(ticket.priority, 'medium')

    def test_str_includes_subject_and_status(self):
        ticket = SupportTicket.objects.create(
            submitted_by=self.user, subject='Broken login', category='it', description='Details'
        )
        self.assertIn('Broken login', str(ticket))
        self.assertIn('open', str(ticket))


class SupportTicketSerializerTests(TestCase):
    def test_missing_category_is_invalid(self):
        s = SupportTicketSerializer(data={'subject': 'Test', 'description': 'Details'})
        self.assertFalse(s.is_valid())
        self.assertIn('category', s.errors)

    def test_missing_description_is_invalid(self):
        s = SupportTicketSerializer(data={'subject': 'Test', 'category': 'it'})
        self.assertFalse(s.is_valid())
        self.assertIn('description', s.errors)

    def test_invalid_category_is_invalid(self):
        s = SupportTicketSerializer(data={
            'subject': 'Test', 'category': 'invalid', 'description': 'Details'
        })
        self.assertFalse(s.is_valid())
        self.assertIn('category', s.errors)

    def test_invalid_priority_is_invalid(self):
        s = SupportTicketSerializer(data={
            'subject': 'Test', 'category': 'it', 'priority': 'urgent', 'description': 'Details'
        })
        self.assertFalse(s.is_valid())
        self.assertIn('priority', s.errors)

    def test_valid_data_passes(self):
        s = SupportTicketSerializer(data={
            'subject': 'Test', 'category': 'it', 'description': 'Details'
        })
        self.assertTrue(s.is_valid())

    def test_status_field_is_read_only(self):
        s = SupportTicketSerializer(data={
            'subject': 'Test', 'category': 'it', 'description': 'Details', 'status': 'resolved'
        })
        self.assertTrue(s.is_valid())
        self.assertNotIn('status', s.validated_data)
