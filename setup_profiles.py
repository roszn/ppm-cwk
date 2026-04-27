import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser
from profiles.models import EmployeeProfile
from datetime import date

admin_email = os.environ.get('ADMIN_EMAIL', 'admin@fdm.com')
admin_password = os.environ.get('ADMIN_PASSWORD', 'Admin123!')
employee_email = os.environ.get('EMPLOYEE_EMAIL', 'john.smith@fdm.com')
employee_password = os.environ.get('EMPLOYEE_PASSWORD', 'Employee123!')

admin, created = CustomUser.objects.get_or_create(
    email=admin_email,
    defaults={
        'username': 'admin',
        'first_name': 'Admin',
        'last_name': 'User',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin.set_password(admin_password)
    admin.save()

employee, created = CustomUser.objects.get_or_create(
    email=employee_email,
    defaults={
        'username': 'jsmith',
        'first_name': 'John',
        'last_name': 'Smith'
    }
)
if created:
    employee.set_password(employee_password)
    employee.save()

EmployeeProfile.objects.filter(user=employee).update(
    job_role='Software Developer',
    department='IT',
    line_manager=admin,
    phone_number='07123456789',
    address='123 Main Street, London',
    date_of_birth=date(1995, 5, 15),
    emergency_contact_name='Jane Smith',
    emergency_contact_phone='07987654321'
)

print("TEST DATA CREATED\n")
