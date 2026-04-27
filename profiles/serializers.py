from rest_framework import serializers
from .models import EmployeeProfile
from accounts.serializers import UserSerializer

class PublicProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = ['id', 'user', 'profile_picture', 'job_role', 'department', 'description', 'about_me']

class PrivateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    line_manager_name = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'user', 'profile_picture', 'job_role', 'department', 'description', 'about_me',
            'line_manager', 'line_manager_name', 'phone_number', 'address',
            'date_of_birth', 'emergency_contact_name', 'emergency_contact_phone', 'salary'
        ]
    
    def get_line_manager_name(self, obj):
        if obj.line_manager:
            name = f"{obj.line_manager.first_name} {obj.line_manager.last_name}".strip()
            return name or obj.line_manager.email
        return None

class UpdatePublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ['profile_picture', 'job_role', 'department', 'description', 'about_me']

    def validate_profile_picture(self, image):
        max_size_mb = 5
        allowed_types = {'image/jpeg', 'image/png', 'image/webp'}

        if image.size > max_size_mb * 1024 * 1024:
            raise serializers.ValidationError(f"Image must be under {max_size_mb}MB.")

        if image.content_type not in allowed_types:
            raise serializers.ValidationError("Only JPEG, PNG, and WebP images are allowed.")

        return image


class AdminUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = [
            'line_manager', 'salary', 'phone_number', 'address',
            'date_of_birth', 'emergency_contact_name', 'emergency_contact_phone'
        ]
