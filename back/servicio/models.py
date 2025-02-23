from django.db import models
from categoria.models import Categoria
from datetime import datetime

# Create your models here.
# def upload_path(instance,filename):
#     return '/'.join(['imagen', str(instance.title),filename])


class Servicio(models.Model):
    id=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='photos/', null=True, blank=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=3)
    fecha_creacion= models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "servicio"
        verbose_name_plural = "servicios"
        verbose_name = "servicio"

    def get_thumbnail(self):
        if self.imagen:
            return self.imagen.url
        return 'imagen.url'

    def __str__(self):
        return self.nombre
