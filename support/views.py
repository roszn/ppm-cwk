from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import SupportTicket
from .serializers import SupportTicketSerializer


class SupportTicketListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = SupportTicket.objects.filter(submitted_by=request.user)
        serializer = SupportTicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SupportTicketSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(submitted_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
