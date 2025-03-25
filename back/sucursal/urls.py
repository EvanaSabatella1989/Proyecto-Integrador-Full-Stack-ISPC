from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from .views import SucursalViewSet
# from sucursal.views import  HorarioSucursal
from . import views



urlpatterns=[
    path('sucursal/', views.listar_sucursales, name='listar_sucursales'),
    # path('horarios/<int:sucursal_id>/', views.obtener_horarios, name='obtener_horarios'),
    # path('modificar-horario/', views.modificar_horario, name='modificar_horario'),
    # path('agregar-horario/', views.agregar_horario, name='agregar_horario'),
    # path('eliminar-horario/<int:horario_id>/', views.eliminar_horario, name='eliminar_horario'),
    # # path('horarios-disponibles/', views.horarios_disponibles, name='horarios_disponibles'),
    # path('horarios-disponibles/<int:sucursal_id>/',horarios_disponibles, name='horarios-disponibles'),
    # path('horarios-reservados/', views.horarios_reservados, name='horarios_reservados')
    # path('',include(router.urls)),
    # path('/horarios/<int:sucursal_id>/<str:fecha>/', views.obtenerHorariosDisponibles, name='horarios-disponibles'),
]