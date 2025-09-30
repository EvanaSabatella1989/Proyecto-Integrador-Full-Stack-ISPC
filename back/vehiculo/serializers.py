from rest_framework import serializers
from .models import Vehiculo
from categoria.models import Categoria

class VehiculoSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    class Meta:
        model = Vehiculo
        fields = '__all__'
        # fields = ['id', 'marca', 'modelo', 'categoria', 'tipo', 'anio_fabricacion', 'cliente']
        
