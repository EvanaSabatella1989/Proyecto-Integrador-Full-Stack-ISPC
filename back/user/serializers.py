from rest_framework import serializers, validators
from django.contrib.auth import get_user_model
User = get_user_model()
from vehiculo.serializers import VehiculoSerializer
from carrito.serializers import CarritoSerializer
from user.models import Cliente
from reserva.serializer import ReservaSerializer

class UserSerializer(serializers.ModelSerializer):
    vehiculos = VehiculoSerializer(many=True, read_only=True, source="cliente.vehiculo_set")
    carrito = CarritoSerializer(read_only=True, source="cliente.carrito")
    reservas = ReservaSerializer(many=True, read_only=True, source="cliente.reserva_set")
    class Meta():
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", 'vehiculos', 'carrito', 'reservas')
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), f"A user with that Email already exists."
                    )
                ],
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        
        #para poder crear usuario en angular
        Cliente.objects.get_or_create(user=user, defaults={'direccion': '', 'num_telefono': ''})
        
        return user
    

class ClienteSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    direccion = serializers.CharField(required=False, allow_blank=True)
    num_telefono = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Cliente
        fields = ['id', 'email', 'first_name', 'last_name', 'direccion', 'num_telefono']

