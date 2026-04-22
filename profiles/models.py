from django.db import models
from accounts.models import CustomUser

class EmployeeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    
    # Public information
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    job_role = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=200, blank=True)
    about_me = models.TextField(blank=True)

    # Private information
    line_manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_employees')
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - Profile"
