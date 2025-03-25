from rest_framework import serializers
from .models import Sucursal
# from sucursal.models import HorarioSucursal


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

# class HorarioSucursalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HorarioSucursal
#         fields = '__all__'