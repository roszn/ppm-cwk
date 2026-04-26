from datetime import date
from django.test import TestCase
from accounts.models import CustomUser
from holiday.models import HolidayRequest, HolidayAllowance
from holiday.serializers import HolidayRequestSerializer, HolidayAllowanceSerializer


class WorkingDaysCalculationTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='u1', email='u1@example.com', password='TestPass123!'
        )

    def _req(self, start, end):
        return HolidayRequest(employee=self.user, start_date=start, end_date=end)

    def test_single_weekday(self):
        # 2026-04-28 is a Tuesday
        self.assertEqual(self._req(date(2026, 4, 28), date(2026, 4, 28))._calc_working_days(), 1)

    def test_weekend_only_returns_zero(self):
        # 2026-04-25 Sat, 2026-04-26 Sun
        self.assertEqual(self._req(date(2026, 4, 25), date(2026, 4, 26))._calc_working_days(), 0)

    def test_full_work_week(self):
        # 2026-04-27 Mon to 2026-05-01 Fri
        self.assertEqual(self._req(date(2026, 4, 27), date(2026, 5, 1))._calc_working_days(), 5)

    def test_two_weeks_spanning_weekends(self):
        # 2026-04-27 Mon to 2026-05-08 Fri = 10 working days
        self.assertEqual(self._req(date(2026, 4, 27), date(2026, 5, 8))._calc_working_days(), 10)

    def test_working_days_persisted_on_save(self):
        req = HolidayRequest(
            employee=self.user, start_date=date(2026, 4, 28), end_date=date(2026, 4, 28)
        )
        req.save()
        self.assertEqual(req.working_days, 1)


class HolidayAllowanceModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='u1', email='u1@example.com', password='TestPass123!'
        )
        self.allowance = HolidayAllowance.objects.create(
            employee=self.user, year=2026, total_days=21
        )

    def test_days_remaining_equals_total_with_no_requests(self):
        self.assertEqual(self.allowance.days_remaining(), 21)

    def test_approved_holiday_reduces_remaining(self):
        HolidayRequest.objects.create(
            employee=self.user, request_type='holiday',
            start_date=date(2026, 4, 28), end_date=date(2026, 4, 30), status='approved'
        )
        self.assertEqual(self.allowance.days_approved(), 3)
        self.assertEqual(self.allowance.days_remaining(), 18)

    def test_pending_holiday_reduces_remaining(self):
        HolidayRequest.objects.create(
            employee=self.user, request_type='holiday',
            start_date=date(2026, 4, 28), end_date=date(2026, 4, 29), status='pending'
        )
        self.assertEqual(self.allowance.days_pending(), 2)
        self.assertEqual(self.allowance.days_remaining(), 19)

    def test_rejected_holiday_does_not_affect_remaining(self):
        HolidayRequest.objects.create(
            employee=self.user, request_type='holiday',
            start_date=date(2026, 4, 28), end_date=date(2026, 5, 1), status='rejected'
        )
        self.assertEqual(self.allowance.days_remaining(), 21)

    def test_absence_not_counted_against_allowance(self):
        HolidayRequest.objects.create(
            employee=self.user, request_type='absence',
            start_date=date(2026, 4, 28), end_date=date(2026, 4, 28), status='approved'
        )
        self.assertEqual(self.allowance.days_approved(), 0)
        self.assertEqual(self.allowance.days_remaining(), 21)


class HolidayRequestSerializerTests(TestCase):
    def test_end_date_before_start_date_is_invalid(self):
        s = HolidayRequestSerializer(data={
            'request_type': 'holiday',
            'start_date': '2026-06-05',
            'end_date': '2026-06-01',
        })
        self.assertFalse(s.is_valid())

    def test_valid_date_range_passes(self):
        s = HolidayRequestSerializer(data={
            'request_type': 'holiday',
            'start_date': '2026-06-01',
            'end_date': '2026-06-05',
        })
        self.assertTrue(s.is_valid())

    def test_same_start_and_end_date_passes(self):
        s = HolidayRequestSerializer(data={
            'request_type': 'holiday',
            'start_date': '2026-06-01',
            'end_date': '2026-06-01',
        })
        self.assertTrue(s.is_valid())


class HolidayAllowanceSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='u1', email='u1@example.com', password='TestPass123!'
        )
        self.allowance = HolidayAllowance.objects.create(
            employee=self.user, year=2026, total_days=10
        )

    def test_computed_fields_reflect_approved_requests(self):
        HolidayRequest.objects.create(
            employee=self.user, request_type='holiday',
            start_date=date(2026, 4, 28), end_date=date(2026, 4, 29), status='approved'
        )
        data = HolidayAllowanceSerializer(self.allowance).data
        self.assertEqual(data['total_days'], 10)
        self.assertEqual(data['days_approved'], 2)
        self.assertEqual(data['days_remaining'], 8)
