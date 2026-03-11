from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = CustomUser.objects.get(email=email)
            
            if user.is_locked:
                raise serializers.ValidationError("Account is locked due to multiple failed login attempts. Contact admin.")
            
            authenticated_user = authenticate(username=email, password=password)
            
            if authenticated_user is None:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 3:
                    user.is_locked = True
                user.save()
                raise serializers.ValidationError("Invalid credentials.")
            
            user.failed_login_attempts = 0
            user.save()
            data['user'] = authenticated_user
            
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")
        
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'is_consultant', 'is_internal_staff']
        read_only_fields = ['id', 'email']
