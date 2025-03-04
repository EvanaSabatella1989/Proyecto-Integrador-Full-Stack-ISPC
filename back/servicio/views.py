from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets,generics,request,status
from .serializer import ServicioSerializer
from .models import Servicio
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny


class ServicioViewSet(viewsets.ModelViewSet):
    queryset=Servicio.objects.all()
    serializer_class=ServicioSerializer
    parser_classes=(MultiPartParser, FormParser,JSONParser)

    @permission_classes([AllowAny])  # Esto hace que la vista sea pública
    def list(self,request):
        # lista todos los servicios
        servicios=self.get_queryset()
        serializer=self.get_serializer(servicios,many=True)
        return Response(serializer.data)
    
    def detail(self,request,pk=None):
        # SOLO UN SERVICIO
        try:
            servicio=self.get_queryset().get(pk=pk)
            serializer=self.get_serializer(servicio)
            return Response(serializer.data)
        except Servicio.DoesNotExist:
            return Response({'error','servicio no encontrado'},status=status.HTTP_404_NOT_FOUND)
        

    def create(self, request):
        # crea un nuevo servicio
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """Actualizar un servicio"""
        try:
            servicio = self.get_queryset().get(pk=pk)
            data = request.data.copy()  # Hacemos una copia de los datos enviados

            if 'imagen' not in data or data['imagen'] == 'null':
                data.pop('imagen', None)  # Si no se envía imagen, se mantiene la existente

            serializer = self.get_serializer(servicio, data=data, partial=True)  # partial=True permite actualizaciones parciales


            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Servicio.DoesNotExist:
            return Response({"error": "Servicio no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        """Eliminar un servicio"""
        try:
            servicio = self.get_queryset().get(pk=pk)
            servicio.delete()
            return Response({"message": "Servicio eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Servicio.DoesNotExist:
            return Response({"error": "Servicio no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# Create your views here.

# me trae todos los servicios
# class ServicioViewSet(viewsets.ModelViewSet):
#     queryset=Servicio.objects.all()
#     serializer_class=ServicioSerializer

# elimina
# class ServicioUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Servicio.objects.all()
#     serializer_class=ServicioSerializer


# @csrf_exempt   #
# @api_view(['GET', 'POST','PUT','DELETE'])
# def servicioList(request, format=None):
#     '''
#     List all code snippets, or create a new snippet.
#     Enumere todos los fragmentos de código o cree uno nuevo.
#     '''
#     if request.method == 'GET':
#         servicio = Servicio.objects.all()
#         serializer = ServicioSerializer(servicio, many=True)
#         # return JsonResponse(serializer.data, safe=False)
#         return Response(serializer.data)


#     elif request.method == 'POST':
        
        # data = JSONParser().parse(request)    
        # data.imagen=request.FILES.get('imagen')
        # serializer = SnippetSerializer(data=data)     #1
      
    #     serializer = ServicioSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    # elif request.method == 'PUT':
    #    if not request.user.is_staff:
    #        return Response({'detail': 'no tienes permiso para realizar esta accion'},
    #                        status=status.HTTP_403_FORBIDDEN)
    #    servicio_id=request.data.get('id')
    #    if not servicio_id:
    #        return Response({'detail':'el campo id es requerido'},status=status.HTTP_400_BAD_REQUEST)
       
    # try:
    #        servicio=Servicio.objects.get(pk=servicio_id)

    # except Servicio.DoesNotExist:
    #        return Response({'detail': 'Servicio no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    # except Servicio.MultipleObjectsReturned:
    #     return Response({'detail': 'Error: múltiples servicios encontrados con el mismo ID.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # serializer=ServicioSerializer(servicio,data=request.data, partial=True)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response({
    #         "message": "Servicio actualizado exitosamente",
    #             "data": serializer.data
    #     }, status=status.HTTP_200_OK)
    # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
           
        # Verifica si el usuario es admin
        # if not request.user.is_staff:
        #     return Response({'detail': 'No tiene permiso para realizar esta acción.'}, 
        #                     status=status.HTTP_403_FORBIDDEN)

        # try:
        #     producto = Servicio.objects.get(pk=request.data.get('id'))
        # except Servicio.DoesNotExist:
        #     return Response({'detail': 'Servicio no encontrado.'}, 
        #                     status=status.HTTP_404_NOT_FOUND)

        # serializer = ServicioSerializer(producto, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
        # elif request.method == 'DELETE':
        # # Verifica si el usuario es admin
        # if not request.user.is_staff:
        #     return Response({'detail': 'No tiene permiso para realizar esta acción.'}, 
        #                     status=status.HTTP_403_FORBIDDEN)

        # try:
        #     producto = Servicio.objects.get(pk=request.data.get('id'))
        # except Servicio.DoesNotExist:
        #     return Response({'detail': 'Servicio no encontrado.'}, 
        #                     status=status.HTTP_404_NOT_FOUND)

        # producto.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
