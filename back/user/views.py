from django.contrib.auth import authenticate
from django.contrib.auth import login as rest_framework_login
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer

# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def login(request):
    email = request.data.get("email", None)
    password = request.data.get("password", None)
    user = authenticate(email=email, password=password)
    print(user)
    if user:
        rest_framework_login(request._request, user)
        token = RefreshToken.for_user(user)
        token['is_admin'] = user.is_staff

        # return Response(data={"access_token": str(token.access_token), "refresh_token": str(token), "is_admin": user.is_staff}, status=status.HTTP_200_OK)
        
        #Modificamos para manejar la sesión de usuario:
        return Response(data={
            "access_token": str(token.access_token),
            "refresh_token": str(token),
            "is_admin": user.is_staff,
            "first_name": user.first_name,  # Agregamos el nombre
            "last_name": user.last_name     # Agregamos el apellido
        }, status=status.HTTP_200_OK)

    return Response(data={"message": "No se encontro ningun usuario"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(data={"message": "El usuario se registro correctamente"})
    return Response(status=status.HTTP_404_NOT_FOUND)
