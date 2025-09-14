from rest_framework import serializers
from rest_framework import serializers
from .models import Reserva,Turno,Servicio
from user.models import Cliente
from user.serializers import ClienteSerializer
from servicio.serializer import ServicioSerializer
from turno.serializers import TurnoSerializer

class ReservaSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    # servicio = ServicioSerializer(read_only=True)
    servicio=serializers.PrimaryKeyRelatedField(queryset=Servicio.objects.all())
    turno = serializers.PrimaryKeyRelatedField(queryset=Turno.objects.all())
    
    class Meta:
        model = Reserva
        fields = '__all__'

     