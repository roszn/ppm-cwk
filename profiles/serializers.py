from rest_framework import serializers
from .models import EmployeeProfile
from accounts.serializers import UserSerializer

class PublicProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = EmployeeProfile
        fields = ['id', 'user', 'profile_picture', 'job_role', 'department']

class PrivateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    line_manager_name = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'user', 'profile_picture', 'job_role', 'department',
            'line_manager', 'line_manager_name', 'phone_number', 'address',
            'date_of_birth', 'emergency_contact_name', 'emergency_contact_phone'
        ]
    
    def get_line_manager_name(self, obj):
        if obj.line_manager:
            return f"{obj.line_manager.first_name} {obj.line_manager.last_name}"
        return None

class UpdatePublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ['profile_picture', 'job_role', 'department']
