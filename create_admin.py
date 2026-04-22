import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

email = os.environ.get('ADMIN_EMAIL', 'admin@fdm.com')
password = os.environ.get('ADMIN_PASSWORD', 'Admin123!')
username = os.environ.get('ADMIN_USERNAME', 'admin')

CustomUser.objects.filter(username=username).delete()
CustomUser.objects.filter(email=email).delete()

admin = CustomUser.objects.create_superuser(
    username=username,
    email=email,
    password=password,
    first_name='Admin',
    last_name='User'
)

print("ADMIN USER CREATED SUCCESSFULLY")
print(f"\nEmail: {email}")
print(f"Is superuser: {admin.is_superuser}")
print(f"Is staff: {admin.is_staff}")
print("\nYou can now login at: http://localhost:8000/admin/")
