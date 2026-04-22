from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import EmployeeProfile
from .serializers import PublicProfileSerializer, PrivateProfileSerializer, UpdatePublicProfileSerializer
from accounts.models import CustomUser

class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile, created = EmployeeProfile.objects.get_or_create(user=request.user)
        serializer = PrivateProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        profile, created = EmployeeProfile.objects.get_or_create(user=request.user)
        serializer = UpdatePublicProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(PrivateProfileSerializer(profile).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        serializer = PublicProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
