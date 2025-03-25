from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from django.core.mail import send_mail
from .serializer import ReservaSerializer
from .models import Reserva,Turno
import logging
from datetime import datetime, timedelta
# from sucursal.models import HorarioSucursal
from rest_framework import status
from user.models import Cliente
from django.conf import settings
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

# SE ENVIA LA RESERVA AL CORREO DEL ADMIN Y CLIENTE
# TAMBIEN SE CONFIRMA LA RESERVA Y SE ENVIA LOS DATOS A LA DB Y EL TURNO DISPONIBLE PASA A FALSE
@api_view(["POST"])
def reservar_turno(request):
    "reservar un turno y enviar los datos al admin por correo"
    if request.method == "POST":
        data = json.loads(request.body)
        cliente_id = data.get("cliente_id")
        turno_id = data.get("turno_id")

        turno = get_object_or_404(Turno, id=turno_id)

        if not turno.disponible:
            return JsonResponse({"error": "Turno no disponible"}, status=400)

        # llamar al cliente
        cliente=get_object_or_404(Cliente,id=cliente_id)
        nombre_cliente=f"{cliente.user.first_name} {cliente.user.last_name}"
        correo_cliente={cliente.user.email}

        #crear la reserva
        reserva = Reserva.objects.create(cliente_id=cliente_id, turno=turno, estado="confirmado")

        # Marcar el turno como no disponible
        # Actualizar el turno a no disponible usando update()
        Turno.objects.filter(id=turno_id).update(disponible=False)
        turno.disponible = False

        turno.save()

        # Enviar correo al admin
        send_mail(
            subject="Nueva Reserva de Turno",
            message=(f"Cliente: {nombre_cliente}\n"
                f"Email: {correo_cliente}\n"
                f"Servicio: {turno.servicio.nombre}\n"
                f"Sucursal: {turno.sucursal.nombre}\n"
                f"Fecha: {turno.fecha}\n"
                f"Hora: {turno.hora}\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["admin@tuempresa.com"]
        )
        # ENVIAR CORREO AL CLIENTE
        send_mail(
            subject="Reserva Confirmada",
            message=f"Tu reserva para el servicio {turno.servicio.nombre} en la sucursal {turno.sucursal.nombre} "
                    f"ha sido confirmada para el día {turno.fecha} a las {turno.hora}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[data.get("cliente_email")]
        )

        return JsonResponse({"message": "Reserva confirmada", "reserva_id": reserva.id}, status=201)

# el cliente elimina el turno reservado
@api_view(["DELETE"])
def eliminar_turno(request, reserva_id):
    if request.method == "DELETE":
        # obtener la reserva
        reserva = get_object_or_404(Reserva, id=reserva_id)
        
        # obtener el turno asociado
        turno = reserva.turno

        # eliminar la reserva
        reserva.delete()

        # marcar el turno como disponible nuevamente
        Turno.objects.filter(id=turno.id).update(disponible=True)

        return JsonResponse({"message": "Reserva eliminada y turno disponible nuevamente"}, status=200)

    return JsonResponse({"error": "Método no permitido"}, status=405)

# @api_view(['POST'])
# def enviarReserva(request):
#     try:
#         # Obtener usuario y cliente
#         user_account = request.user  # Usuario autenticado
#         cliente = Cliente.objects.get(user=user_account)  # Obtener cliente relacionado con el usuario

#         # Obtener el ID del turno de la solicitud
#         turno_id = request.data.get('turno')  # Cambié 'turno_id' por 'turno'

#         if not turno_id:
#             return Response({"error": "El campo 'turno' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

#         # Verificar si el turno existe
#         turno = get_object_or_404(Turno, id=turno_id)

#         # Verificar si el turno está disponible
#         if not turno.disponible:
#             return Response({"error": "El turno ya está reservado."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Crear la reserva
#         reserva = Reserva(cliente=cliente, turno=turno)
#         reserva.save()

#         # Actualizar disponibilidad del turno
#         turno.disponible = False
#         turno.save()

#         # Enviar correo al administrador
#         send_mail(
#             subject="Nueva reserva de turno realizada",
#             message=f"Se reservó un turno \n\nDetalles:\n"
#                     f"- Cliente: {cliente.user.get_full_name()}\n"
#                     f"- Correo: {cliente.user.email}\n"
#                     f"- Teléfono: {cliente.num_telefono}\n"
#                     f"- Servicio: {turno.servicio}\n"
#                     f"- Sucursal: {turno.sucursal}\n"
#                     f"- Fecha: {turno.fecha}\n"
#                     f"- Hora: {turno.hora}",
#             from_email="autoservicebsas@gmail.com",
#             recipient_list=["autoservicebsas@gmail.com"],
#             fail_silently=False,
#         )

#         # Devolver la respuesta con los datos de la reserva
#         return Response(ReservaSerializer(reserva).data, status=status.HTTP_201_CREATED)

#     except Cliente.DoesNotExist:
#         return Response({"error": "El usuario no tiene un perfil de cliente."}, status=status.HTTP_400_BAD_REQUEST)
#     except Turno.DoesNotExist:
#         return Response({"error": "El turno seleccionado no existe."}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({"error": f"Ocurrió un error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


































# @api_view(['POST'])
# def enviarReserva(request):
#     try:
#         user_account=request.user   #usuario registrado
#         cliente=Cliente.objects.get(user=user_account)  #obtener cliente relacionado con el usuario
#         turno_id=request.data.get(user=user_account)
#         turno=get_object_or_404(Turno,id=turno_id)
#         if not turno.disponible:
#             return Response({"error":"el turno ya esta reservado"},status=status.HTTP_404_NOT_FOUND)
        
#         # guardo en la base de datos
#         reserva=Reserva(cliente=cliente,turno=turno)
#         reserva.save()

#         # se avisa que el turno no esta mas disponible
#         turno.disponible=False
#         turno.save()

#         # se envia el correo al administrador
#         send_mail(
#             subject="Nueva reserva de turno realizada",
#             message=f"Se reservo un turno \n\nDetalles:\n"
#             f"- Cliente: {cliente.user.get_full_name()}\n"
#             f"- Correo: {cliente.user.email}\n"
#             f"- Teléfono: {cliente.num_telefono}\n"
#             f"- Servicio: {turno.servicio}\n"
#             f"- Sucursal: {turno.sucursal}\n"
#             f"- Fecha: {turno.fecha}\n"
#             f"- Hora: {turno.hora}",
#             from_email="autoservicebsas@gmail.com",
#             recipient_list=["autoservicebsas@gmail.com"],
#             fail_silently=False,
#         )
#         return Response(ReservaSerializer(reserva).data, status=status.HTTP_201_CREATED)
#     except Cliente.DoesNotExist:
#         return Response({"error": "El usuario no tiene un perfil de cliente."}, status=status.HTTP_400_BAD_REQUEST)
#     except Turno.DoesNotExist:
#         return Response({"error": "El turno seleccionado no existe."}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({"error": f"Ocurrió un error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
#funciona con la tabla horario sucursal
#  @api_view(['POST'])
# def reserva(request):
#     try:
#         print(request.data)
#         # Buscar la fecha y hora de la sucursal
#         fecha = HorarioSucursal.objects.get(id=request.data['fecha_sucursal'])
#         hora = HorarioSucursal.objects.get(id=request.data['hora_sucursal'])

#         # Verificar disponibilidad del horario
#         if not fecha.disponible or not hora.disponible:
            
#             return Response({'error': 'Este horario ya está reservado'}, status=status.HTTP_400_BAD_REQUEST)

#         # Marcarlo como reservado
#         fecha.disponible = False
#         hora.disponible = False
#         fecha.save()
#         hora.save()

#         # Guardar la reserva
#         serializer = ReservaSerializer(data=request.data)
#         if serializer.is_valid():
#             reserva = serializer.save()

#             # Enviar correo con la información de la reserva
#             send_mail(
#                 'Nueva Reserva de Turno',
#                 f"""
#                 Nombre: {reserva.nombre_cliente}
#                 Email: {reserva.correo_cliente}
#                 Fecha: {reserva.fecha_sucursal.fecha} a las {reserva.hora_sucursal.hora}
#                 Servicio: {reserva.servicio.nombre}
#                 Sucursal: {reserva.sucursal.nombre}
#                 """,
#                 'autoservicebsas@gmail.com',
#                 ['autoservicebsas@gmail.com'],
#                 fail_silently=False,
#             )

#             return Response({'message': 'Reserva de turno enviada'}, status=200)
#         else:
#             print(request.data)
#             return Response(serializer.errors, status=400)

#     except Exception as e:
#         logger.error(f"Error en la reserva: {e}")
#         return Response({'error': str(e)}, status=500)




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