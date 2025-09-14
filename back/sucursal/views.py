from django.shortcuts import render
from rest_framework import viewsets, status
from reserva.models import Reserva
from .models import Sucursal
from .serializers import SucursalSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging
from django.shortcuts import render,get_object_or_404
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from django.db.models import Prefetch
# from sucursal.models import HorarioSucursal

logger = logging.getLogger(__name__)

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer

    



