from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from carrito.models import Carrito, CarritoItem
from producto.models import Producto
from .serializers import CarritoSerializer
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_carrito(request):
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    serializer = CarritoSerializer(carrito)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def agregar_al_carrito(request):
    user = request.user
    producto_id = request.data.get('producto_id')
    cantidad = request.data.get('cantidad', 1)

    carrito, created = Carrito.objects.get_or_create(user=user)
    producto = Producto.objects.get(id=producto_id)
    
    item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        item.cantidad += int(cantidad)
        item.save()

    return Response({"message": "Producto agregado al carrito"}, status=status.HTTP_200_OK)

# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def eliminar_del_carrito(request, item_id):
#     try:
#         item = CarritoItem.objects.get(id=item_id, carrito__user=request.user)
#         item.delete()
#         return Response({"message": "Producto eliminado"}, status=status.HTTP_200_OK)
#     except CarritoItem.DoesNotExist:
#         return Response({"error": "Producto no encontrado en el carrito"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_del_carrito(request, producto_id):
    try:
        item = CarritoItem.objects.get(producto__id=producto_id, carrito__user=request.user)
        item.delete()
        return Response({"message": "Producto eliminado del carrito"}, status=status.HTTP_200_OK)
    except CarritoItem.DoesNotExist:
        return Response({"error": "El producto no está en el carrito"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def modificar_cantidad_carrito(request):
    user = request.user
    producto_id = request.data.get('producto_id')
    nueva_cantidad = request.data.get('cantidad')

    if not producto_id or not nueva_cantidad:
        return Response({"error": "Se requiere producto_id y cantidad"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        carrito = Carrito.objects.get(user=user)
        item = CarritoItem.objects.get(carrito=carrito, producto_id=producto_id)
        item.cantidad = int(nueva_cantidad)
        item.save()
        return Response({"message": "Cantidad actualizada correctamente"}, status=status.HTTP_200_OK)
    except CarritoItem.DoesNotExist:
        return Response({"error": "Producto no encontrado en el carrito"}, status=status.HTTP_404_NOT_FOUND)