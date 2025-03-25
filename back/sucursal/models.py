from django.db import models
from django.core.validators import RegexValidator
from datetime import time
from datetime import date



# Create your models here.

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, default='')
    latitud = models.FloatField(default=0.0)
    longitud = models.FloatField(default=0.0)

    def __str__(self):
        return self.nombre
    

class Meta:
        db_table = "sucursal"
        verbose_name_plural = "sucursales"
        verbose_name = "sucursal"
    
def __str__(self):
        return f"{self.sucursal.nombre} :{self.sucursal.direccion}"

# class Sucursal(models.Model):
#     direccion = models.CharField(max_length=100)
#     telefono_regex = RegexValidator(
#         regex=r'^\+?1?\d{9,15}$',
#         message="El número de teléfono debe estar en el formato: '+999999999'."
#     )
#     telefono = models.CharField(
#         max_length=15,
#         validators=[telefono_regex],
#         unique=True
#     )
#     email = models.EmailField()

#     class Meta:
#         db_table = "sucursal"
#         verbose_name_plural = "sucursales"
#         verbose_name = "sucursal"

#     def __str__(self):
#         return self.direccion


# class HorarioSucursal(models.Model):
#     sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="horarios")
#     fecha = models.DateField(default=date.today) 
#     hora = models.TimeField(null=True, blank=True) 
#     # hora_cierre =models.TimeField(null=True, blank=True)
#     disponible = models.BooleanField(default=True)


# class Meta:
#     db_table = "horario_sucursal"
#     verbose_name_plural = "horario_sucursales"
#     verbose_name = "horario_sucursal"


    # def __str__(self):
    #     return f"{self.sucursal.nombre} :{self.sucursal.direccion}: {self.fecha}: {self.hora} : {self.fecha} : {self.disponible}"

