import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

# Delete existing test employee if exists
CustomUser.objects.filter(username='jsmith').delete()
CustomUser.objects.filter(email='john.smith@fdm.com').delete()

# Create regular employee
employee = CustomUser.objects.create_user(
    username='jsmith',
    email='john.smith@fdm.com',
    password='Employee123!',
    first_name='John',
    last_name='Smith'
)

print("EMPLOYEE USER CREATED SUCCESSFULLY\n")
print(f"Email: john.smith@fdm.com")
print(f"Password: Employee123!")
print(f"Is staff: {employee.is_staff}")
print(f"Is superuser: {employee.is_superuser}")
print(f"Is locked: {employee.is_locked}")
print("\nNow test login at: http://localhost:8000/api/auth/login/")
