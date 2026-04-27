import random
from datetime import date, timedelta, time
from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from shifts.models import Shift

# Rotation of realistic shift patterns: (start, end)
SHIFT_PATTERNS = [
    (time(9, 0),  time(17, 0)),   # standard
    (time(8, 0),  time(16, 0)),   # early
    (time(10, 0), time(18, 0)),   # late
    (time(7, 30), time(15, 30)),  # early start
    (time(8, 30), time(16, 30)),  # mid
]


class Command(BaseCommand):
    help = 'Seeds dummy shift data for all users (weekdays only, Apr–Dec 2026)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing shifts before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            deleted, _ = Shift.objects.all().delete()
            self.stdout.write(f'Cleared {deleted} existing shifts.')

        users = list(CustomUser.objects.all())
        if not users:
            self.stdout.write(self.style.WARNING('No users found. Create users first.'))
            return

        # Give each user a consistent base pattern so their schedule looks realistic
        user_patterns = {u.pk: SHIFT_PATTERNS[i % len(SHIFT_PATTERNS)] for i, u in enumerate(users)}

        start = date(2026, 4, 1)
        end = date(2026, 12, 31)
        current = start
        created = 0

        while current <= end:
            if current.weekday() < 5:   # Mon–Fri only
                for user in users:
                    base = user_patterns[user.pk]
                    # 10 % chance of a different pattern to add variety
                    pattern = random.choice(SHIFT_PATTERNS) if random.random() < 0.1 else base
                    _, was_created = Shift.objects.get_or_create(
                        employee=user,
                        date=current,
                        defaults={'start_time': pattern[0], 'end_time': pattern[1]},
                    )
                    if was_created:
                        created += 1
            current += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS(
            f'Done. Created {created} shifts for {len(users)} user(s).'
        ))
