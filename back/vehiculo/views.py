from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Vehiculo
from .serializers import VehiculoSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agregar_vehiculo(request):
    if request.method == 'POST':
        vehiculo_data = {
            'marca': request.data.get('marca'),
            'modelo': request.data.get('modelo'),
            'categoria': request.data.get('categoria'),
            'tipo': request.data.get('tipo'),
            'anio_fabricacion': request.data.get('anio_fabricacion'),
            'cliente': request.user.cliente.id  # Asumiendo que el cliente está relacionado con el usuario autenticado
        }

        vehiculo_serializer = VehiculoSerializer(data=vehiculo_data)
        
        if vehiculo_serializer.is_valid():
            vehiculo_serializer.save()
            return Response({'message': 'Vehículo agregado exitosamente'}, status=status.HTTP_201_CREATED)
        else:
            return Response(vehiculo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)