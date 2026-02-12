from django.urls import path
from .views import CheckInView

urlpatterns = [
    path('checkin/', CheckInView.as_view()),
]