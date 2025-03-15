from django.db import models
from sucursal.models import Sucursal


# Create your models here.


class Turno(models.Model):
    fecha = models.DateTimeField()
    hora = models.TimeField()
    ESTADOS_TURNO = (
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    )
    estado_turno = models.CharField(max_length=20, choices=ESTADOS_TURNO)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    class Meta:
        db_table = "turno"
        verbose_name_plural = "turnos"
        verbose_name = "turno"

    def __str__(self):
        return self.id