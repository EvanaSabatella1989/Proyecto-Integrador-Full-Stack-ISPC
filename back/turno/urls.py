from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TurnoViewSet
from .views import turnos_disponibles

router = DefaultRouter()
router.register(r"turnos", TurnoViewSet,basename='turnos')

urlpatterns=[path('',include(router.urls)),
             path('disponibles/<int:sucursal_id>/', turnos_disponibles, name='turnos_disponibles'),]