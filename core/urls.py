from django.urls import path
from .views import CheckInView, MemberInfoView

urlpatterns = [
    path('checkin/', CheckInView.as_view()),
    path('member/<str:qr>/', MemberInfoView.as_view()),
]
