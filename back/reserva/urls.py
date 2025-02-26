from django.urls import path
from .views import reserva
from reserva import views


urlpatterns = [
    path('reserva/', reserva, name='reserva'),
]