from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import EmployeeProfile
from .serializers import PublicProfileSerializer, PrivateProfileSerializer, UpdatePublicProfileSerializer, AdminUpdateProfileSerializer
from accounts.models import CustomUser


class ProfilePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile, created = EmployeeProfile.objects.get_or_create(user=request.user)
        serializer = PrivateProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        profile, _ = EmployeeProfile.objects.get_or_create(user=request.user)

        public_serializer = UpdatePublicProfileSerializer(profile, data=request.data, partial=True)
        if not public_serializer.is_valid():
            return Response(public_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        public_serializer.save()

        if request.user.is_staff:
            private_serializer = AdminUpdateProfileSerializer(profile, data=request.data, partial=True)
            if not private_serializer.is_valid():
                return Response(private_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            private_serializer.save()

        return Response(PrivateProfileSerializer(profile).data, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            profile = EmployeeProfile.objects.get(user=user)

            if request.user.id == user_id or request.user.is_staff:
                serializer = PrivateProfileSerializer(profile)
            else:
                serializer = PublicProfileSerializer(profile)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (CustomUser.DoesNotExist, EmployeeProfile.DoesNotExist):
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class AllProfilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = EmployeeProfile.objects.all()
        paginator = ProfilePagination()
        page = paginator.paginate_queryset(profiles, request)
        serializer = PublicProfileSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
