from django.db import models
from accounts.models import CustomUser


class Content(models.Model):
    TYPE_CHOICES = [
        ('news', 'News'),
        ('file', 'File'),
        ('policy', 'Policy'),
        ('update', 'Update'),
    ]

    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    content_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='news')
    file = models.FileField(upload_to='content_files/', null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='uploaded_content')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title
