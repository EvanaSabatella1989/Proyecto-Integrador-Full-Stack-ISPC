from rest_framework import serializers
from .models import Sucursal
# from sucursal.models import HorarioSucursal


class SucursalSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Sucursal
        fields = '__all__'

