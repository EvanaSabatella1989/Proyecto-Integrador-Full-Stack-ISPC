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
from django.core.mail import send_mail
from .serializer import ReservaSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def reserva(request):
    try:
        # Intenta deserializar los datos y guardar la reserva
        serializer = ReservaSerializer(data=request.data)

        if serializer.is_valid():
            reserva = serializer.save()  # Guarda la reserva y obtiene el objeto

            # Enviar correo con Mailtrap
            send_mail(
                'Nueva Reserva de Turno',
                f"""
                Nombre: {reserva.nombre}
                Email: {reserva.email}
                Teléfono: {reserva.telefono}
                Fecha del Turno: {reserva.fecha.strftime}
                Servicio: {reserva.servicio.nombre}
                Sucursal: {reserva.sucursal.direccion}
                Descripción: {reserva.descripcion}
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
