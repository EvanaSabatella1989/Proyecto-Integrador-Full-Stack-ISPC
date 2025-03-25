from django.db import models
from sucursal.models import Sucursal
from servicio.models import Servicio

class Turno(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, default=1)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default=1)
    fecha = models.DateField()
    hora = models.TimeField()
    disponible = models.BooleanField(default=True)


class Meta:
        db_table = "turno"
        verbose_name_plural = "turnos"
        verbose_name = "turno"

def __str__(self):
        return f"{self.servicio} - {self.fecha} {self.hora}"

# # Create your models here.


# class Turno(models.Model):
#     fecha = models.DateTimeField()
#     hora = models.TimeField()
#     ESTADOS_TURNO = (
#         ('pendiente', 'Pendiente'),
#         ('confirmado', 'Confirmado'),
#         ('cancelado', 'Cancelado'),
#     )
#     estado_turno = models.CharField(max_length=20, choices=ESTADOS_TURNO)
#     sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

#     class Meta:
#         db_table = "turno"
#         verbose_name_plural = "turnos"
#         verbose_name = "turno"

#     def __str__(self):
#         return self.id