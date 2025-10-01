from rest_framework import serializers
from .models import Servicio
from categoria.models import Categoria

class ServicioSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(required=False)  #  que la imagen no sea obligatoria
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    class Meta:
        model=Servicio
        fields='__all__'
        depth = 1
        

#para que traiga el nombre del servicio    
# class ServicioNombreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Servicio
#         fields = ['id', 'nombre', 'precio']  
