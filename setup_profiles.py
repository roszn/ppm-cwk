import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser
from profiles.models import EmployeeProfile
from datetime import date

# Get or create admin
admin, created = CustomUser.objects.get_or_create(
    email='admin@fdm.com',
    defaults={
        'username': 'admin',
        'first_name': 'Admin',
        'last_name': 'User',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin.set_password('Admin123!')
    admin.save()

# Get or create employee
employee, created = CustomUser.objects.get_or_create(
    email='john.smith@fdm.com',
    defaults={
        'username': 'jsmith',
        'first_name': 'John',
        'last_name': 'Smith'
    }
)
if created:
    employee.set_password('Employee123!')
    employee.save()

# Create profile for employee
profile, created = EmployeeProfile.objects.get_or_create(
    user=employee,
    defaults={
        'job_role': 'Software Developer',
        'department': 'IT',
        'line_manager': admin,
        'phone_number': '07123456789',
        'address': '123 Main Street, London',
        'date_of_birth': date(1995, 5, 15),
        'emergency_contact_name': 'Jane Smith',
        'emergency_contact_phone': '07987654321'
    }
)

print("TEST DATA CREATED\n")
