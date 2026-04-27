from django.test import TestCase
from accounts.models import CustomUser
from content.models import Content
from content.serializers import ContentSerializer


class ContentModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='u1', email='u1@example.com', password='TestPass123!'
        )

    def test_str_returns_title(self):
        c = Content(title='My Article', content_type='news')
        self.assertEqual(str(c), 'My Article')

    def test_pinned_content_ordered_before_unpinned(self):
        Content.objects.create(title='Normal', content_type='news', uploaded_by=self.user)
        Content.objects.create(title='Pinned', content_type='policy', is_pinned=True, uploaded_by=self.user)
        first = Content.objects.first()
        self.assertEqual(first.title, 'Pinned')


class ContentSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='u1', email='u1@example.com', password='TestPass123!',
            first_name='Jane', last_name='Doe'
        )

    def test_uploaded_by_name_uses_full_name(self):
        content = Content.objects.create(
            title='Article', content_type='news', uploaded_by=self.user
        )
        data = ContentSerializer(content).data
        self.assertEqual(data['uploaded_by_name'], 'Jane Doe')

    def test_uploaded_by_name_falls_back_to_email(self):
        no_name = CustomUser.objects.create_user(
            username='u2', email='u2@example.com', password='TestPass123!'
        )
        content = Content.objects.create(
            title='Article', content_type='news', uploaded_by=no_name
        )
        data = ContentSerializer(content).data
        self.assertEqual(data['uploaded_by_name'], 'u2@example.com')

    def test_uploaded_by_name_is_none_with_no_uploader(self):
        content = Content.objects.create(title='Article', content_type='news', uploaded_by=None)
        data = ContentSerializer(content).data
        self.assertIsNone(data['uploaded_by_name'])

    def test_missing_title_is_invalid(self):
        s = ContentSerializer(data={'content_type': 'news'})
        self.assertFalse(s.is_valid())
        self.assertIn('title', s.errors)

    def test_invalid_content_type_is_invalid(self):
        s = ContentSerializer(data={'title': 'Article', 'content_type': 'invalid'})
        self.assertFalse(s.is_valid())
        self.assertIn('content_type', s.errors)
