from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_consultant', 'is_internal_staff', 'is_locked')
    search_fields = ('email', 'username')
    list_filter = ('is_consultant', 'is_internal_staff', 'is_locked')
# Register your models here.
