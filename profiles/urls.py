from django.urls import path
from .views import MyProfileView, UserProfileView, AllProfilesView

urlpatterns = [
    path('me/', MyProfileView.as_view(), name='my-profile'),
    path('all/', AllProfilesView.as_view(), name='all-profiles'),
    path('<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
]
