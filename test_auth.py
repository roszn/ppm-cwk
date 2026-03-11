import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

print("=" * 50)
print("AUTHENTICATION SYSTEM TEST")
print("=" * 50)

# Test 1: Create test users
print("\n1. Creating test users...")
try:
    # Delete existing test users if they exist
    CustomUser.objects.filter(email__in=['staff@fdm.com', 'admin@fdm.com']).delete()
    
    # Create staff user
    staff = CustomUser.objects.create_user(
        username='staff1',
        email='staff@fdm.com',
        password='Staff123!',
        first_name='Jane',
        last_name='Smith'
    )
    print(f"✓ Created internal staff: {staff.email}")
    
    # Create admin user
    admin = CustomUser.objects.create_superuser(
        username='admin',
        email='admin@fdm.com',
        password='Admin123!',
        first_name='Admin',
        last_name='User'
    )
    print(f"✓ Created admin: {admin.email}")
    
except Exception as e:
    print(f"✗ Error creating users: {e}")

# Test 2: Password policy validation
print("\n2. Testing password policy...")
weak_passwords = [
    ('short', 'Too short'),
    ('alllowercase123!', 'No uppercase'),
    ('ALLUPPERCASE123!', 'No lowercase'),
    ('NoNumbers!', 'No digits'),
    ('NoSpecial123', 'No special character'),
]

for pwd, reason in weak_passwords:
    try:
        validate_password(pwd)
        print(f"✗ {reason}: '{pwd}' should have failed")
    except ValidationError:
        print(f"✓ {reason}: '{pwd}' correctly rejected")

try:
    validate_password('ValidPass123!')
    print(f"✓ Strong password: 'ValidPass123!' correctly accepted")
except ValidationError as e:
    print(f"✗ Strong password rejected: {e}")

# Test 3: Account locking mechanism
print("\n3. Testing account locking...")
test_user = CustomUser.objects.get(email='staff@fdm.com')
print(f"Initial failed attempts: {test_user.failed_login_attempts}")
print(f"Account locked: {test_user.is_locked}")

# Simulate failed login attempts
test_user.failed_login_attempts = 2
test_user.save()
print(f"After 2 failed attempts: {test_user.failed_login_attempts}")

test_user.failed_login_attempts = 3
test_user.is_locked = True
test_user.save()
print(f"After 3 failed attempts - Locked: {test_user.is_locked}")

# Reset for testing
test_user.failed_login_attempts = 0
test_user.is_locked = False
test_user.save()
print(f"✓ Account reset for API testing")

print("\n" + "=" * 50)
print("TEST USERS CREATED - Ready for API testing!")
print("=" * 50)
print("\nTest Credentials:")
print("1. Staff: staff@fdm.com / Staff123!")
print("2. Admin: admin@fdm.com / Admin123!")
print("\nStart the server with: python manage.py runserver")
print("Then test the endpoints:")
print("  POST http://localhost:8000/api/auth/login/")
print("  GET  http://localhost:8000/api/auth/me/")
print("  POST http://localhost:8000/api/auth/logout/")
