import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

# Delete existing admin if exists
CustomUser.objects.filter(username='admin').delete()
CustomUser.objects.filter(email='admin@fdm.com').delete()

# Create superuser
admin = CustomUser.objects.create_superuser(
    username='admin',
    email='admin@fdm.com',
    password='Admin123!',
    first_name='Admin',
    last_name='User'
)

print("=" * 50)
print("ADMIN USER CREATED SUCCESSFULLY")
print("=" * 50)
print(f"Email: admin@fdm.com")
print(f"Password: Admin123!")
print(f"Is superuser: {admin.is_superuser}")
print(f"Is staff: {admin.is_staff}")
print("\nYou can now login at: http://localhost:8000/admin/")
