import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

email = os.environ.get('EMPLOYEE_EMAIL', 'john.smith@fdm.com')
password = os.environ.get('EMPLOYEE_PASSWORD', 'Employee123!')
username = os.environ.get('EMPLOYEE_USERNAME', 'jsmith')

CustomUser.objects.filter(username=username).delete()
CustomUser.objects.filter(email=email).delete()

employee = CustomUser.objects.create_user(
    username=username,
    email=email,
    password=password,
    first_name='John',
    last_name='Smith'
)

print("EMPLOYEE USER CREATED SUCCESSFULLY\n")
print(f"Email: {email}")
print(f"Is staff: {employee.is_staff}")
print(f"Is superuser: {employee.is_superuser}")
print(f"Is locked: {employee.is_locked}")
print("\nNow test login at: http://localhost:8000/api/auth/login/")
