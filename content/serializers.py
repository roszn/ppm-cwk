from rest_framework import serializers
from .models import Content


class ContentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'title', 'body', 'content_type', 'file', 'is_pinned', 'uploaded_by_name', 'created_at']
        read_only_fields = ['id', 'uploaded_by_name', 'created_at']

    def get_uploaded_by_name(self, obj):
        if obj.uploaded_by:
            name = f"{obj.uploaded_by.first_name} {obj.uploaded_by.last_name}".strip()
            return name or obj.uploaded_by.email
        return None
