from django.db import models
from turno.models import Turno
from user.models import Cliente
    
class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,null=True, blank=True) 
    turno = models.OneToOneField(Turno,on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=20,
        choices=[("pendiente", "Pendiente"), ("confirmado", "Confirmado"), ("cancelado", "Cancelado")],
        default="pendiente",
    )

class Meta:
    db_table = "reserva"
    verbose_name_plural = "reservas"
    verbose_name = "reserva"


def save(self, *args, **kwargs):
        """forzar la lógica de confirmación al guardar la reserva"""
        if self.estado == "confirmado":
            self.turno.disponible = False
            self.turno.save()
        super().save(*args, **kwargs)


def __str__(self):  
        return f"reserva para {self.cliente}el dia {self.turno}"





# from sucursal.models import Sucursal
# from servicio.models import Servicio
# from sucursal.models import HorarioSucursal

# class Reserva(models.Model):
#     # usuario = models.ForeignKey(User, on_delete=models.CASCADE)
#     sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
#     servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
#     hora_sucursal = models.ForeignKey(HorarioSucursal, on_delete=models.CASCADE,related_name='reservas_fecha',default=1 )
#     fecha_sucursal=models.ForeignKey(HorarioSucursal,on_delete=models.CASCADE,related_name='reservas_hora',default=1 )
#     nombre_cliente = models.CharField(max_length=100)
#     correo_cliente = models.EmailField(default='default@example.com')


# class Meta:
#     db_table = "reserva"
#     verbose_name_plural = "reservas"
#     verbose_name = "reserva"


#     def __str__(self):
#         return f"Reserva de {self.nombre_cliente} en {self.sucursal.nombre} el {self.hora_sucursal.hora} a las {self.fecha_sucursal.fecha} para el servicio de {self.servicio.nombre}"

