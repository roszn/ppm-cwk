from django.urls import path
from .views import HolidayRequestListView, HolidayRequestDetailView, TeamRequestsView, HolidayAllowanceView

urlpatterns = [
    path('', HolidayRequestListView.as_view(), name='holiday-list'),
    path('<int:request_id>/', HolidayRequestDetailView.as_view(), name='holiday-detail'),
    path('team/', TeamRequestsView.as_view(), name='holiday-team'),
    path('allowance/', HolidayAllowanceView.as_view(), name='holiday-allowance'),
]
