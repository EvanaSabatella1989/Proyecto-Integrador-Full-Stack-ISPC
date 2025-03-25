from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Turno
from .serializers import TurnoSerializer
from django.http import JsonResponse


class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer

# @action(detail=False, methods=["get"])
# def disponibles(self, request):
#     turnos = Turno.objects.filter(disponible=True)
#     serializer = self.get_serializer(turnos, many=True)
#     return Response(serializer.data)
def turnos_disponibles(request, sucursal_id):
    turnos = Turno.objects.filter(sucursal_id=sucursal_id, disponible=True).order_by('fecha', 'hora')
    turnos_data = [
        {"id": t.id, "fecha": t.fecha, "hora": t.hora.strftime("%H:%M"), "sucursal": t.sucursal.nombre,"servicio":t.servicio.nombre}
        for t in turnos
    ]
    return JsonResponse(turnos_data, safe=False)