from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password as check_hash
from .models import CustomUser

# Used to equalise timing when the email doesn't exist, preventing enumeration.
_DUMMY_HASH = 'pbkdf2_sha256$600000$dummysaltvalue$dummyhashvalue='

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
            check_hash(password, _DUMMY_HASH)  # equalise timing to prevent email enumeration
            raise serializers.ValidationError("Invalid credentials.")
        
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'email']
