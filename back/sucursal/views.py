from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Sucursal
from .serializers import SucursalSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [AllowAny]  # permisos aplicados a toda la vista

    def list(self, request):
        #lista todas las sucursales
        sucursales = self.get_queryset()
        serializer = self.get_serializer(sucursales, many=True)
        return Response(serializer.data)

    def create(self, request):
        #crea una nueva sucursal
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Error al crear sucursal: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            sucursal = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(sucursal, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            logger.error(f"Error al actualizar sucursal {pk}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Sucursal.DoesNotExist:
            return Response({"error": "Sucursal no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            sucursal = self.get_queryset().get(pk=pk)
            sucursal.delete()
            return Response({"message": "Sucursal eliminada correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Sucursal.DoesNotExist:
            return Response({"error": "Sucursal no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error al eliminar sucursal {pk}: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
