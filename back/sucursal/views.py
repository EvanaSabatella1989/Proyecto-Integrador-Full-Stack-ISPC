from django.shortcuts import render
from rest_framework import viewsets, status
from reserva.models import Reserva
from .models import Sucursal
# from .serializers import SucursalSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging
from django.shortcuts import render,get_object_or_404
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from django.db.models import Prefetch
from sucursal.serializers import SucursalReadSerializer,SucursalWriteSerializer 
# from sucursal.models import HorarioSucursal
from rest_framework.decorators import action

logger = logging.getLogger(__name__)

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return SucursalReadSerializer   # devuelve nombres de servicios
        return SucursalWriteSerializer      # recibe IDs de servicios


 # endpoint para sucursales por servicio
    @action(detail=False, methods=['get'], url_path='por-servicio')
    def por_servicio(self, request):
        servicio_id = request.query_params.get('servicio_id')
        sucursales = Sucursal.objects.filter(servicios__id=servicio_id)
        serializer = SucursalReadSerializer(sucursales, many=True)
        return Response(serializer.data)
