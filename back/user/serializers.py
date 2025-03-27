from rest_framework import serializers, validators
from django.contrib.auth import get_user_model
User = get_user_model()
from vehiculo.serializers import VehiculoSerializer
from carrito.serializers import CarritoSerializer


class UserSerializer(serializers.ModelSerializer):
    vehiculos = VehiculoSerializer(many=True, read_only=True, source="cliente.vehiculo_set")
    carrito = CarritoSerializer(read_only=True, source="cliente.carrito")
    class Meta():
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", 'vehiculos', 'carrito')
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
        return user
