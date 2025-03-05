from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from .views import SucursalViewSet

router=DefaultRouter()
router.register(r'sucursal', SucursalViewSet, basename='sucursal')

urlpatterns=[
    path('',include(router.urls)),
]