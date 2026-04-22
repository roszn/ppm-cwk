from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import HolidayRequest, HolidayAllowance
from .serializers import HolidayRequestSerializer, HolidayAllowanceSerializer


class HolidayRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = HolidayRequest.objects.filter(employee=request.user)
        serializer = HolidayRequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HolidayRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # enforce holiday allowance for holiday (not absence) requests
        if request.data.get('request_type', 'holiday') == 'holiday':
            year = serializer.validated_data['start_date'].year
            allowance, _ = HolidayAllowance.objects.get_or_create(
                employee=request.user, year=year, defaults={'total_days': 21}
            )
            # calculate working days before saving
            from datetime import timedelta
            start = serializer.validated_data['start_date']
            end = serializer.validated_data['end_date']
            days_requested = sum(
                1 for i in range((end - start).days + 1)
                if (start + timedelta(days=i)).weekday() < 5
            )
            if days_requested > allowance.days_remaining():
                return Response(
                    {'error': f"Insufficient allowance. You have {allowance.days_remaining()} days remaining."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer.save(employee=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HolidayRequestDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_request(self, request_id):
        try:
            return HolidayRequest.objects.get(id=request_id)
        except HolidayRequest.DoesNotExist:
            return None

    def delete(self, request, request_id):
        hr = self._get_request(request_id)
        if not hr:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        if hr.employee != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        if hr.status != 'pending':
            return Response({'error': 'Only pending requests can be cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        hr.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, request_id):
        hr = self._get_request(request_id)
        if not hr:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        # only the employee's line manager or staff can approve/reject
        is_line_manager = (
            hasattr(hr.employee, 'profile') and
            hr.employee.profile.line_manager == request.user
        )
        if not (request.user.is_staff or is_line_manager):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        if new_status not in ('approved', 'rejected'):
            return Response({'error': 'Status must be approved or rejected'}, status=status.HTTP_400_BAD_REQUEST)

        hr.status = new_status
        hr.reviewed_by = request.user
        hr.reviewed_at = timezone.now()
        hr.save()
        return Response(HolidayRequestSerializer(hr).data)


class TeamRequestsView(APIView):
    """Pending requests where I am the line manager."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = HolidayRequest.objects.filter(
            employee__profile__line_manager=request.user,
            status='pending',
        ).select_related('employee')
        serializer = HolidayRequestSerializer(requests, many=True)
        return Response(serializer.data)


class HolidayAllowanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = int(request.query_params.get('year', timezone.now().year))
        allowance, _ = HolidayAllowance.objects.get_or_create(
            employee=request.user, year=year, defaults={'total_days': 21}
        )
        serializer = HolidayAllowanceSerializer(allowance)
        return Response(serializer.data)
