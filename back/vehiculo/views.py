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

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def vehiculo_detalle(request, pk):
    try:
        vehiculo = Vehiculo.objects.get(pk=pk, cliente=request.user.cliente)
    except Vehiculo.DoesNotExist:
        return Response({'error': 'Vehículo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VehiculoSerializer(vehiculo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        vehiculo_data = {
            'marca': request.data.get('marca', vehiculo.marca),
            'modelo': request.data.get('modelo', vehiculo.modelo),
            'categoria': request.data.get('categoria', vehiculo.categoria),
            'tipo': request.data.get('tipo', vehiculo.tipo),
            'anio_fabricacion': request.data.get('anio_fabricacion', vehiculo.anio_fabricacion),
            'cliente': request.user.cliente.id
        }

        serializer = VehiculoSerializer(vehiculo, data=vehiculo_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Vehículo actualizado correctamente'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_vehiculo(request, id):
    try:
        vehiculo = Vehiculo.objects.get(id=id, cliente=request.user.cliente)  # solo permite eliminar si pertenece al usuario
        vehiculo.delete()
        return Response({'message': 'Vehículo eliminado correctamente'}, status=status.HTTP_200_OK)
    except Vehiculo.DoesNotExist:
        return Response({'error': 'Vehículo no encontrado o no permitido'}, status=status.HTTP_404_NOT_FOUND)