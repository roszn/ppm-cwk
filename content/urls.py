from django.urls import path
from .views import ContentListView, ContentDetailView

urlpatterns = [
    path('', ContentListView.as_view(), name='content-list'),
    path('<int:content_id>/', ContentDetailView.as_view(), name='content-detail'),
]
