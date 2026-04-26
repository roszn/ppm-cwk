from django.db import models
from accounts.models import CustomUser


class BankHoliday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(unique=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.name} ({self.date})"


class Shift(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shifts')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee.email} — {self.date} {self.start_time}–{self.end_time}"
