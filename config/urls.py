from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import LogoutRedirectView
from accounts.test_views import login_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('api/content/', include('content.urls')),
    path('api/holiday/', include('holiday.urls')),
    path('api/support/', include('support.urls')),
    path('', login_page, name='login'),
    path('login', login_page, name='login-alt'),
    path('homepage', TemplateView.as_view(template_name='homepage.html'), name='homepage'),
    path('profile', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('support', TemplateView.as_view(template_name='support.html'), name='support'),
    path('holiday', TemplateView.as_view(template_name='holiday.html'), name='holiday'),
    path('logout', LogoutRedirectView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
