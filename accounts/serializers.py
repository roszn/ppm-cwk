from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'is_consultant', 'is_internal_staff')
        read_only_fields = ('id',)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'is_consultant')
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    