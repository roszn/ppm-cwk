from datetime import date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from holiday.models import HolidayRequest
from .models import BankHoliday, Shift
from .serializers import BankHolidaySerializer, ShiftSerializer, CalendarHolidaySerializer


def _current_month_range():
    today = date.today()
    start = today.replace(day=1)
    # last day of month
    next_month = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
    end = next_month - timedelta(days=1)
    return start, end


class CalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        raw_start = request.query_params.get('start')
        raw_end = request.query_params.get('end')
        default_start, default_end = _current_month_range()

        try:
            start_date = date.fromisoformat(raw_start) if raw_start else default_start
            end_date = date.fromisoformat(raw_end) if raw_end else default_end
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if end_date < start_date:
            return Response(
                {'error': 'end must be on or after start.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # staff can view any employee via ?user_id=
        target_user_id = request.query_params.get('user_id')
        if target_user_id and request.user.is_staff:
            try:
                target_user_id = int(target_user_id)
            except ValueError:
                return Response({'error': 'Invalid user_id.'}, status=status.HTTP_400_BAD_REQUEST)
            shift_qs = Shift.objects.filter(employee_id=target_user_id, date__range=(start_date, end_date))
            holiday_qs = HolidayRequest.objects.filter(
                employee_id=target_user_id,
                start_date__lte=end_date,
                end_date__gte=start_date,
                status__in=['approved', 'pending'],
            )
        elif request.user.is_staff and not target_user_id:
            shift_qs = Shift.objects.filter(date__range=(start_date, end_date)).select_related('employee')
            holiday_qs = HolidayRequest.objects.filter(
                start_date__lte=end_date,
                end_date__gte=start_date,
                status__in=['approved', 'pending'],
            ).select_related('employee')
        else:
            shift_qs = Shift.objects.filter(employee=request.user, date__range=(start_date, end_date))
            holiday_qs = HolidayRequest.objects.filter(
                employee=request.user,
                start_date__lte=end_date,
                end_date__gte=start_date,
                status__in=['approved', 'pending'],
            )

        bank_holidays = BankHoliday.objects.filter(date__range=(start_date, end_date))

        return Response({
            'range': {'start': start_date, 'end': end_date},
            'bank_holidays': BankHolidaySerializer(bank_holidays, many=True).data,
            'shifts': ShiftSerializer(shift_qs, many=True).data,
            'holidays': CalendarHolidaySerializer(holiday_qs, many=True).data,
        })
