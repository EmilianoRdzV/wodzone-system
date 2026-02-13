from django.urls import path
from .views import CheckInView
from . import views

urlpatterns = [
    path('checkin/', CheckInView.as_view()),
    path('', views.home, name='home'),
]