from django.urls import path
from .views import CovidAPIView

urlpatterns = [
    path('',CovidAPIView.as_view(),name='cases'),
]