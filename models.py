# yourapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Login portal user.

    Notes:
    - password hashing is handled by Django automatically via set_password()/check_password()
    - `password` and `last_login` fields are already provided by AbstractUser
    """

    # Your migration has email unique=True
    email = models.EmailField(unique=True)
    
    # Login security controls (matches your migration)
    failed_login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)

    # Optional flags (these were in your migration; keep only if you want them)
    is_consultant = models.BooleanField(default=False)
    is_internal_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username