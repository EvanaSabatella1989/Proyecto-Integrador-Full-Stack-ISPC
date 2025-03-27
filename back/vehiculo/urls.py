from django.urls import path
from . import views

urlpatterns = [
    path('vehiculo/agregar/', views.agregar_vehiculo, name='agregar_vehiculo'),
]