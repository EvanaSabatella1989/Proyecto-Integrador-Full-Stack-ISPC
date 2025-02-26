from rest_framework import serializers

from .models import Reserva

class ReservaSerializer(serializers.ModelSerializer):
    fecha = serializers.DateTimeField(format="%Y-%m-%dT%H:%M", input_formats=["%Y-%m-%dT%H:%M"])  # solo año, mes, dia y hora
    class Meta:
        model = Reserva
        fields = '__all__'