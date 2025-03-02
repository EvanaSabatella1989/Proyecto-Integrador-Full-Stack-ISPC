from django.db import models
from servicio.models import Servicio
from sucursal.models import Sucursal
from user.models import Cliente

# Create your models here.


class Reserva(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(default='default@example.com')
    telefono = models.CharField(max_length=20,null=True, blank=True)
    fecha= models.DateTimeField()
    descripcion = models.TextField(blank=True, null=True)


    class Meta:
        db_table = "reserva"
        verbose_name_plural = "reservas"
        verbose_name = "reserva"

    def save(self, *args, **kwargs):
        # para que fecha solo tenga año, mes, dia y hora 
        self.fecha = self.fecha.replace(second=0, microsecond=0)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.estado_reserva