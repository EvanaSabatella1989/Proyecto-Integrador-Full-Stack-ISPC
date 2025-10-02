from rest_framework import serializers
from .models import Servicio
from categoria.models import Categoria

class ServicioSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(required=False)  #  que la imagen no sea obligatoria
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    class Meta:
        model=Servicio
        fields='__all__'
<<<<<<< HEAD
        # depth = 1
        
=======
        depth = 1
        

#para que traiga el nombre del servicio    
# class ServicioNombreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Servicio
#         fields = ['id', 'nombre', 'precio']  
>>>>>>> 0885bcdb20f7dff55d88a842507f494cfa53e432
