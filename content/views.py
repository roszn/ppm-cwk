from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Content
from .serializers import ContentSerializer


class ContentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = Content.objects.all()
        serializer = ContentSerializer(content, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ContentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, content_id):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        try:
            content = Content.objects.get(id=content_id)
            content.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Content.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
