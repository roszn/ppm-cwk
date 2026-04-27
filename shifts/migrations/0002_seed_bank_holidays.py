from datetime import date
from django.db import migrations

# England & Wales bank holidays for 2025 and 2026
BANK_HOLIDAYS = [
    # 2025
    ("New Year's Day",          date(2025, 1,  1)),
    ("Good Friday",             date(2025, 4, 18)),
    ("Easter Monday",           date(2025, 4, 21)),
    ("Early May Bank Holiday",  date(2025, 5,  5)),
    ("Spring Bank Holiday",     date(2025, 5, 26)),
    ("Summer Bank Holiday",     date(2025, 8, 25)),
    ("Christmas Day",           date(2025, 12, 25)),
    ("Boxing Day",              date(2025, 12, 26)),
    # 2026
    ("New Year's Day",          date(2026, 1,  1)),
    ("Good Friday",             date(2026, 4,  3)),
    ("Easter Monday",           date(2026, 4,  6)),
    ("Early May Bank Holiday",  date(2026, 5,  4)),
    ("Spring Bank Holiday",     date(2026, 5, 25)),
    ("Summer Bank Holiday",     date(2026, 8, 31)),
    ("Christmas Day",           date(2026, 12, 25)),
    ("Boxing Day",              date(2026, 12, 28)),
]


def seed(apps, schema_editor):
    BankHoliday = apps.get_model('shifts', 'BankHoliday')
    for name, d in BANK_HOLIDAYS:
        BankHoliday.objects.get_or_create(date=d, defaults={'name': name})


def unseed(apps, schema_editor):
    BankHoliday = apps.get_model('shifts', 'BankHoliday')
    BankHoliday.objects.filter(date__year__in=[2025, 2026]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
