# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from django.core.mail import send_mail
# from .serializer import ReservaSerializer
# import logging
# logger = logging.getLogger(__name__)



# # Create your views here.
# @api_view(['POST'])
# def reserva(request):
#     try:
#         # Intenta deserializar los datos y guardar la reserva
#         serializer = ReservaSerializer(data=request.data)
        
#         if serializer.is_valid():
#             # Guarda la reserva si es válida
#             serializer.save()

#            # enviar correo con Mailtrap
#             send_mail(
#                 'Nueva Reserva de Turno',
#                 f"Nombre: {request.data['nombre']}\nEmail: {request.data['email']}\nTeléfono: {request.data['telefono']}\nFecha del Turno: {request.data['fecha']}\nDescripción: {request.data['descripcion']}",
#                 'autoservicebsas@gmail.com',#un correo ficticio
#                 ['autoservicebsas@gmail.com'],#para donde debe ir
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
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from django.core.mail import send_mail
from .serializer import ReservaSerializer
from .models import Reserva
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer


# @api_view(['POST'])
# def reserva(request):
#     try:
#          # Intenta deserializar los datos y guardar la reserva
#         serializer = ReservaSerializer(data=request.data)

#         if serializer.is_valid():
#             reserva = serializer.save()  # Guarda la reserva y obtiene el objet

#              # datos de la reserva enviar correo con Mailtrap
#             send_mail(
#                 "Nueva Reserva de Servicio"
#              f"""
#              Se ha realizado una nueva reserva:
#             - Cliente: {reserva.nombre}
#             - Servicio: {reserva.servicio.nombre}
#             - Fecha: {reserva.fecha_reserva}
#             - Hora: {reserva.hora_reserva}
#             - Sucursal: {reserva.sucursal.direccion}
#             """

#             ,
#             'autoservicebsas@gmail.com',  # correo desde el cual se enviará el email
#             ['autoservicebsas@gmail.com'],  #correo del administrador
#             fail_silently=False,
#         )
#         # Respuesta exitosa
#             return Response({'message': 'Reserva de turno enviada'}, status=200)
#         else:
#             # Respuesta en caso de que la validación del serializer falle
#             return Response(serializer.errors, status=400)

#     except Exception as e:
#         # Manejo de excepciones: si ocurre un error en el proceso
#         logger.error(f"Error en la reserva: {e}")
#         return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def obtenerHorariosDisponibles(request, sucursal_id, fecha):
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Formato de fecha inválido. Use AAAA-MM-DD."},status=400)
    
    #definir el rango de los horarios de las reservas
    horarios_posibles=[timedelta(hours=h) for h in range(9, 18)]

    # busca horarios ya reservados en la base de datos
    reservas=Reserva.objects.filter(fecha_reserva=fecha_obj,sucursal_id=sucursal_id)
    horarios_ocupados={reserva.hora_reserva for reserva in reservas}

    #filtrar horarios disponibles
    horarios_disponibles=[
       (datetime.combine(fecha_obj, datetime.min.time()) + h).time() 
        for h in horarios_posibles if (datetime.combine(fecha_obj, datetime.min.time()) + h).time() not in horarios_ocupados
    ]
    return Response({"fecha": fecha, "horarios_disponibles": horarios_disponibles})


@api_view(['POST'])
def reserva(request):
    try:
        # Intenta deserializar los datos y guardar la reserva
        serializer = ReservaSerializer(data=request.data)

        if serializer.is_valid():
            # Verificar si ya existe una reserva para el mismo horario y sucursal
            data = serializer.validated_data
            fecha_reserva = data['fecha_reserva']
            hora_reserva = data['hora_reserva']
            sucursal = data['sucursal']

            # Comprobar si ya hay una reserva para ese horario
            if Reserva.objects.filter(fecha_reserva=fecha_reserva, hora_reserva=hora_reserva, sucursal=sucursal).exists():
                return Response({"error": "El horario ya está reservado."}, status=400)

            reserva = serializer.save()  # Guarda la reserva y obtiene el objeto

            # Enviar correo con la información de la reserva
            send_mail(
                'Nueva Reserva de Turno',
                f"""
                Nombre: {reserva.nombre}
                Email: {reserva.email}
                Fecha:{reserva.fecha_reserva}
                Hora: {reserva.hora_reserva}
                Servicio: {reserva.servicio.nombre}
                Sucursal: {reserva.sucursal.direccion}
                """,
                'autoservicebsas@gmail.com',  # Correo ficticio
                ['autoservicebsas@gmail.com'],  # Para donde debe ir
                fail_silently=False,
            )

            # Respuesta exitosa
            return Response({'message': 'Reserva de turno enviada'}, status=200)
        else:
            # Respuesta en caso de que la validación del serializer falle
            return Response(serializer.errors, status=400)

    except Exception as e:
        # Manejo de excepciones: si ocurre un error en el proceso
        logger.error(f"Error en la reserva: {e}")
        return Response({'error': str(e)}, status=500)