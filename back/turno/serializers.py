from rest_framework import serializers
from .models import Turno

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        hora = serializers.TimeField(format="%H:%M")  # formato para solo mostrar horas y minutos
        model = Turno
        fields = ['id', 'fecha', 'hora', 'sucursal', 'servicio', 'disponible']


        def create(self, validated_data):
        # al guardar el turno, asegúrate de que la hora sea solo con minutos
            hora = validated_data.get('hora')
        # ajusta la hora para eliminar los segundos
            validated_data['hora'] = hora.replace(second=0)
            return super().create(validated_data)




      