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
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated] 
    
# SE ENVIA LA RESERVA AL CORREO DEL ADMIN Y CLIENTE
# TAMBIEN SE CONFIRMA LA RESERVA Y SE ENVIA LOS DATOS A LA DB Y EL TURNO DISPONIBLE PASA A FALSE
    def perform_create(self, serializer):
    
        logger.debug(f"📥 Datos validados recibidos: {serializer.validated_data}")
        self.reservar_turno(serializer)

    def reservar_turno(self, serializer):
       
        try:
            user = self.request.user
            cliente = Cliente.objects.get(user=user)
            reserva = serializer.save(cliente=cliente)
            turno = serializer.validated_data['turno']
            logger.debug(f"Intentando reservar horario ID={turno.id} | Fecha={turno.fecha} | Hora={turno.hora}")

            if not turno.disponible:
                logger.warning(f"Horario ID={turno.id} ya estaba reservado.")
                raise serializers.ValidationError("Este horario ya está reservado")

            # horario como no disponible
            turno.disponible = False
            turno.save()
            logger.info(f"Horario ID={turno.id} marcado como no disponible.")

           
            

            # obtener datos del cliente
            cliente=reserva.cliente
            nombre_cliente=cliente.user.get_full_name()
            correo_cliente=cliente.user.email
            
             # se guarda la reserva
            reserva = serializer.save(cliente=cliente)
            
            logger.info(f"Reserva creada con éxito ID={reserva.id} para cliente {nombre_cliente}")

            # envio correo
            try:
                send_mail(
                    'Nueva Reserva de Turno',
                    f"""
                    Nombre: {nombre_cliente}
                    Email: {correo_cliente}
                    Fecha: {turno.fecha} a las {turno.hora}
                    Servicio: {reserva.servicio.nombre}
                    Sucursal: {turno.sucursal.nombre}
                    """,
                    'autoservicebsas@gmail.com',
                    ['autoservicebsas@gmail.com'],
                    fail_silently=False,
                )
                logger.info(f"Correo enviado correctamente para la reserva ID={reserva.id}")
            except Exception as e:
                logger.error(f"Error enviando correo para la reserva ID={reserva.id}: {str(e)}")

        except Exception as e:
            logger.exception(f"Error creando reserva: {str(e)}")
            raise

