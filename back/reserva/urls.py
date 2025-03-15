from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservaViewSet,reserva
from .views import Reserva




urlpatterns = [
    
    
   
    path('reserva/', reserva, name="reserva"),  # Ruta personalizada para la reserva
]