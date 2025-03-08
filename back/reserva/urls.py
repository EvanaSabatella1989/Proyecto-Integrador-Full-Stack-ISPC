from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservaViewSet, obtenerHorariosDisponibles,reserva
from .views import Reserva



urlpatterns = [
    
    
    path('disponibilidad/<int:sucursal_id>/<str:fecha>/', obtenerHorariosDisponibles, name="horarios-disponibles"),
    path('reserva/', reserva, name="reserva"),  # Ruta personalizada para la reserva
]