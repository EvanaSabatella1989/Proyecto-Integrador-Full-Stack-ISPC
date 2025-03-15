from django.shortcuts import render
from rest_framework import viewsets, status
from reserva.models import Reserva
from .models import Sucursal
from .serializers import SucursalSerializer,HorarioSucursalSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging
from django.shortcuts import render,get_object_or_404
from datetime import datetime, timedelta
from rest_framework.decorators import api_view

from sucursal.models import HorarioSucursal

logger = logging.getLogger(__name__)

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [AllowAny]  # permisos aplicados a toda la vista




#  todas las sucursales
@api_view(['GET'])
def listar_sucursales(request):
    sucursales = Sucursal.objects.all()
    serializer = SucursalSerializer(sucursales, many=True)
    return Response(serializer.data)


# horarios disponibles de una sucursal
@api_view(['GET'])
def obtener_horarios(request, sucursal_id):
    horarios = HorarioSucursal.objects.filter(sucursal_id=sucursal_id, disponible=True)
    serializer = HorarioSucursalSerializer(horarios, many=True)
    return Response(serializer.data)


# modificar disponibilidad de un horario
@api_view(['POST'])
def modificar_horario(request):
    try:
        horario = HorarioSucursal.objects.get(id=request.data['id'])
        horario.disponible = request.data['disponible']
        horario.save()
        return Response({'message': 'Horario actualizado'}, status=status.HTTP_200_OK)
    except HorarioSucursal.DoesNotExist:
        return Response({'error': 'Horario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    

# sgregar un nuevo horario
@api_view(['POST'])
def agregar_horario(request):
    serializer = HorarioSucursalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Eliminar un horario
@api_view(['DELETE'])
def eliminar_horario(request, horario_id):
    try:
        horario = HorarioSucursal.objects.get(id=horario_id)
        horario.delete()
        return Response({'message': 'Horario eliminado'}, status=status.HTTP_200_OK)
    except HorarioSucursal.DoesNotExist:
        return Response({'error': 'Horario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    

# horarios disponibles en las sucursales
@api_view(['GET'])
def horarios_disponibles(request):
    """
    Devuelve todos los horarios disponibles de todas las sucursales.
    """
    try:
        horarios = HorarioSucursal.objects.filter(disponible=True).order_by('fecha', 'hora')

        if not horarios.exists():
            return Response({'message': 'No hay horarios disponibles en ninguna sucursal.'}, status=status.HTTP_200_OK)

        serializer = HorarioSucursalSerializer(horarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



@api_view(['GET'])
def horarios_reservados(request):
    # mensaje en la api
    """
    Lista de  todos los horarios reservados de todas las sucursales.
    """
    try:
        horarios = HorarioSucursal.objects.filter(disponible=False).order_by('fecha', 'hora')

        if not horarios.exists():
            return Response({'message': 'No hay horarios reservados en ninguna sucursal.'}, status=status.HTTP_200_OK)

        serializer = HorarioSucursalSerializer(horarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
















#     def list(self, request):
#         #lista todas las sucursales
#         sucursales = self.get_queryset()
#         serializer = self.get_serializer(sucursales, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         #crea una nueva sucursal
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         logger.error(f"Error al crear sucursal: {serializer.errors}")
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, pk=None):
#         try:
#             sucursal = self.get_queryset().get(pk=pk)
#             serializer = self.get_serializer(sucursal, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             logger.error(f"Error al actualizar sucursal {pk}: {serializer.errors}")
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Sucursal.DoesNotExist:
#             return Response({"error": "Sucursal no encontrada"}, status=status.HTTP_404_NOT_FOUND)

#     def destroy(self, request, pk=None):
#         try:
#             sucursal = self.get_queryset().get(pk=pk)
#             sucursal.delete()
#             return Response({"message": "Sucursal eliminada correctamente"}, status=status.HTTP_204_NO_CONTENT)
#         except Sucursal.DoesNotExist:
#             return Response({"error": "Sucursal no encontrada"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             logger.error(f"Error al eliminar sucursal {pk}: {e}")
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['GET'])
# def obtenerHorariosDisponibles(request, sucursal_id, fecha):
#     try:
#         fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
#     except ValueError:
#         return Response({"error": "Formato de fecha inválido. Use AAAA-MM-DD."},status=400)
    
#     # verifica si existe sucursal
#     sucursal=get_object_or_404(Sucursal, id=sucursal_id)

#     # obtener el dia de la semaña
#     dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
#     dia_actual = dias_semana[fecha_obj.weekday()]

#     # obtener el horario de la sucursal para ese dia
#     horario = HorarioSucursal.objects.filter(sucursal=sucursal, dia=dia_actual).first()

#     if not horario:
#         return Response({"error": "La sucursal no tiene horarioss para este dia."}, status=400)
    
#     # se genera los horarios disponibles dentro de los horarios de apertuta y cierre
#     hora_actual = datetime.combine(fecha_obj, horario.hora_apertura)
#     hora_final = datetime.combine(fecha_obj, horario.hora_cierre)
#     intervalo = timedelta(minutes=60)  # los turnos son cada 60 minutos

#     horarios_posibles = []
#     while hora_actual < hora_final:
#         horarios_posibles.append(hora_actual.time())
#         hora_actual += intervalo

#     # busca que horarios estan reservados
#     reservas = Reserva.objects.filter(fecha_reserva=fecha_obj, sucursal=sucursal)
#     horarios_ocupados = {reserva.hora_reserva for reserva in reservas}

#     # busca los horarios disponibles
#     horarios_disponibles = [hora for hora in horarios_posibles if hora not in horarios_ocupados]

#     return Response({"fecha": fecha, "horarios_disponibles": horarios_disponibles})