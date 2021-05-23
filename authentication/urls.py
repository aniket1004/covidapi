from django.urls import  path
from .views import RegistrationView, VerifyEmail, LoginAPIView,LogoutAPIView
from rest_framework_simplejwt.views import (TokenRefreshView,)

urlpatterns = [
    path ('register/',RegistrationView.as_view(),name="register"),
    path('email-verify/',VerifyEmail.as_view(),name='email-verify'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('logout/',LogoutAPIView.as_view(),name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]