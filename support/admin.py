from django.contrib import admin
from .models import SupportTicket


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'submitted_by', 'subject', 'category', 'priority', 'status', 'created_at']
    list_filter = ['status', 'category', 'priority']
    search_fields = ['submitted_by__email', 'subject']
    list_editable = ['status']
