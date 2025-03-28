from django.db import models
from django.core.validators import RegexValidator
from datetime import time
from datetime import date

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

