from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from .views import SucursalViewSet
# from sucursal.views import  HorarioSucursal
from . import views



urlpatterns=[
    path('sucursal/', views.listar_sucursales, name='listar_sucursales'),
    
]