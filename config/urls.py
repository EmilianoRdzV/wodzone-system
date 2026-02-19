from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')), # <--- Aquí conectamos tu app
    #path('', include('core.urls')),
    path('memberinfo/<str:qr>/', views.muestraInfo, name='muestraInfo')
]