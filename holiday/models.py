from django.db import models
from accounts.models import CustomUser


class HolidayAllowance(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='allowances')
    year = models.IntegerField()
    total_days = models.IntegerField(default=21)

    class Meta:
        unique_together = ('employee', 'year')

    def days_approved(self):
        return sum(
            r.working_days for r in self.employee.holiday_requests.filter(
                status='approved',
                request_type='holiday',
                start_date__year=self.year,
            )
        )

    def days_pending(self):
        return sum(
            r.working_days for r in self.employee.holiday_requests.filter(
                status='pending',
                request_type='holiday',
                start_date__year=self.year,
            )
        )

    def days_remaining(self):
        return self.total_days - self.days_approved() - self.days_pending()

    def __str__(self):
        return f"{self.employee.email} — {self.year} ({self.total_days} days)"


class HolidayRequest(models.Model):
    TYPE_CHOICES = [
        ('holiday', 'Holiday'),
        ('absence', 'Absence'),
    ]
    ABSENCE_CHOICES = [
        ('illness', 'Illness'),
        ('dentist', 'Dentist Appointment'),
        ('medical', 'Medical Appointment'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='holiday_requests')
    request_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='holiday')
    absence_reason = models.CharField(max_length=20, choices=ABSENCE_CHOICES, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    working_days = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_requests'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.working_days = self._calc_working_days()
        super().save(*args, **kwargs)

    def _calc_working_days(self):
        from datetime import timedelta
        count = 0
        current = self.start_date
        while current <= self.end_date:
            if current.weekday() < 5:  # Mon–Fri
                count += 1
            current += timedelta(days=1)
        return count

    def __str__(self):
        return f"{self.employee.email} — {self.request_type} {self.start_date} to {self.end_date}"
