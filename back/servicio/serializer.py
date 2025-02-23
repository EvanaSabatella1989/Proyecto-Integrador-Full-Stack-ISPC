from rest_framework import serializers
from .models import Servicio

class ServicioSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(required=False)  #  que la imagen no sea obligatoria
    class Meta:
        model=Servicio
        fields=['id','nombre','imagen','descripcion','precio','fecha_creacion']
