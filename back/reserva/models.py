# from django.db import models
# from servicio.models import Servicio
# from sucursal.models import Sucursal
# from user.models import Cliente

# # Create your models here.

from django.db import models
from sucursal.models import Sucursal
from servicio.models import Servicio
from sucursal.models import HorarioSucursal

class Reserva(models.Model):
    # usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    horario = models.ForeignKey(HorarioSucursal, on_delete=models.CASCADE)
    nombre_cliente = models.CharField(max_length=100)
    correo_cliente = models.EmailField(default='default@example.com')


class Meta:
    db_table = "reserva"
    verbose_name_plural = "reservas"
    verbose_name = "reserva"


    def __str__(self):
        return f"Reserva de {self.nombre_cliente} en {self.sucursal.nombre} el {self.horario.fecha} a las {self.horario.hora}"
# class Reserva(models.Model):
#     nombre = models.CharField(max_length=255, null=True, blank=True)
#     email = models.EmailField(default='default@example.com')
#     telefono = models.CharField(max_length=20,null=True, blank=True)
#     fecha= models.DateTimeField()
#     descripcion = models.TextField(blank=True, null=True)


#     class Meta:
#         db_table = "reserva"
#         verbose_name_plural = "reservas"
#         verbose_name = "reserva"

#     def save(self, *args, **kwargs):
#         # para que fecha solo tenga año, mes, dia y hora 
#         self.fecha = self.fecha.replace(second=0, microsecond=0)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.estado_reserva


# esta opcion funciona
# from django.db import models
# from servicio.models import Servicio
# from sucursal.models import Sucursal

# class Reserva(models.Model):
#     nombre = models.CharField(max_length=255, null=True, blank=True)
#     email = models.EmailField(default='default@example.com')
#     # telefono = models.CharField(max_length=20, null=True, blank=True)
#     fecha_reserva = models.DateField()
#     hora_reserva = models.TimeField()
#     # descripcion = models.TextField(blank=True, null=True)

#     # Relacionar con Servicio y Sucursal
#     servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
#     sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

#     class Meta:
#         db_table = "reserva"
#         # constraints = [
#         #     models.UniqueConstraint(fields=['fecha_reserva', 'hora_reserva', 'sucursal'], name='unique_reservation')#UniqueConstraintpermite que no reservas duplicadas
#         # ]
#     def save(self, *args, **kwargs):
#         # Ajustar la fecha para que solo tenga año, mes, día y hora
#         self.hora_reserva = self.hora_reserva.replace(second=0, microsecond=0)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Reserva de {self.nombre} - {self.servicio.nombre} en {self.sucursal.nombre} el dia {self.fecha_reserva} a las {self.hora_reserva}"
