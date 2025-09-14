from rest_framework import serializers
from .models import Turno
from sucursal.serializers import SucursalSerializer

class TurnoSerializer(serializers.ModelSerializer):
    sucursal = SucursalSerializer(read_only=True)

    class Meta:
        model = Turno
        fields = '__all__'




      