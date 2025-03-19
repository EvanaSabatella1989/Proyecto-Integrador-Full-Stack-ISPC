from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from django.core.mail import send_mail
from .serializer import ReservaSerializer
from .models import Reserva
import logging
from datetime import datetime, timedelta
from sucursal.models import HorarioSucursal
from rest_framework import status

logger = logging.getLogger(__name__)

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer


@api_view(['POST'])
def reserva(request):
    try:
        print(request.data)
        # Buscar la fecha y hora de la sucursal
        fecha = HorarioSucursal.objects.get(id=request.data['fecha_sucursal'])
        hora = HorarioSucursal.objects.get(id=request.data['hora_sucursal'])

        # Verificar disponibilidad del horario
        if not fecha.disponible or not hora.disponible:
            
            return Response({'error': 'Este horario ya está reservado'}, status=status.HTTP_400_BAD_REQUEST)

        # Marcarlo como reservado
        fecha.disponible = False
        hora.disponible = False
        fecha.save()
        hora.save()

        # Guardar la reserva
        serializer = ReservaSerializer(data=request.data)
        if serializer.is_valid():
            reserva = serializer.save()

            # Enviar correo con la información de la reserva
            send_mail(
                'Nueva Reserva de Turno',
                f"""
                Nombre: {reserva.nombre_cliente}
                Email: {reserva.correo_cliente}
                Fecha: {reserva.fecha_sucursal.fecha} a las {reserva.hora_sucursal.hora}
                Servicio: {reserva.servicio.nombre}
                Sucursal: {reserva.sucursal.nombre}
                """,
                'autoservicebsas@gmail.com',
                ['autoservicebsas@gmail.com'],
                fail_silently=False,
            )

            return Response({'message': 'Reserva de turno enviada'}, status=200)
        else:
            print(request.data)
            return Response(serializer.errors, status=400)

    except Exception as e:
        logger.error(f"Error en la reserva: {e}")
        return Response({'error': str(e)}, status=500)




# esta opcion funciona
# @api_view(['POST'])
# def reserva(request):
#     try:
#         # Intenta deserializar los datos y guardar la reserva
#         serializer = ReservaSerializer(data=request.data)

#         if serializer.is_valid():
#             # Verificar si ya existe una reserva para el mismo horario y sucursal
#             data = serializer.validated_data
#             fecha_reserva = data['fecha_reserva']
#             hora_reserva = data['hora_reserva']
#             sucursal = data['sucursal']

#             # Comprobar si ya hay una reserva para ese horario
#             if Reserva.objects.filter(fecha_reserva=fecha_reserva, hora_reserva=hora_reserva, sucursal=sucursal).exists():
#                 return Response({"error": "El horario ya está reservado."}, status=400)

#             reserva = serializer.save()  # Guarda la reserva y obtiene el objeto

#             # Enviar correo con la información de la reserva
#             send_mail(
#                 'Nueva Reserva de Turno',
#                 f"""
#                 Nombre: {reserva.nombre}
#                 Email: {reserva.email}
#                 Fecha:{reserva.fecha_reserva}
#                 Hora: {reserva.hora_reserva}
#                 Servicio: {reserva.servicio.nombre}
#                 Sucursal: {reserva.sucursal.direccion}
#                 """,
#                 'autoservicebsas@gmail.com',  # Correo ficticio
#                 ['autoservicebsas@gmail.com'],  # Para donde debe ir
#                 fail_silently=False,
#             )

#             # Respuesta exitosa
#             return Response({'message': 'Reserva de turno enviada'}, status=200)
#         else:
#             # Respuesta en caso de que la validación del serializer falle
#             return Response(serializer.errors, status=400)

#     except Exception as e:
#         # Manejo de excepciones: si ocurre un error en el proceso
#         logger.error(f"Error en la reserva: {e}")
#         return Response({'error': str(e)}, status=500)