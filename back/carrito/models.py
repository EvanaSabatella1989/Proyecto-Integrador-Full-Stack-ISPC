from django.db import models
from user.models import UserAccount
from producto.models import Producto  # Asegúrate de tener este modelo

class Carrito(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    
    def total_precio(self):
        return sum(item.total_precio() for item in self.items.all())

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def total_precio(self):
        return self.producto.precio * self.cantidad
