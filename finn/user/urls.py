from django.urls import path, include
from .views import register, account, profile, change_password

urlpatterns = [
    path('', include('django.contrib.auth.urls')),  # login, logout, password reset
    path('register/', register, name='register'),
    path('account/', account, name='account'),
    path('profile/', profile, name='profile'),
    path('change-password/', change_password, name='change_password'),
]