from django.contrib import admin
from .models import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'is_pinned', 'uploaded_by', 'created_at']
    list_filter = ['content_type', 'is_pinned']
    search_fields = ['title', 'body']
