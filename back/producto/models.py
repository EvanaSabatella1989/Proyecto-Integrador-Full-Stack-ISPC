from django.db import models
from categoria.models import Categoria
from datetime import datetime

# Create your models here.




class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    # imagen = models.ImageField(upload_to='photos/')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True) # Cloudinary maneja el upload
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    date_created = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "producto"
        verbose_name_plural = "productos"
        verbose_name = "producto"

    def get_thumbnail(self):
        if self.imagen:
            return self.imagen.url
        return 'imagen.url'

    # def get_absolute_image_url(self):
    #     if self.imagen:
    #         return f"{settings.MEDIA_URL}{self.imagen}"
    #     return ""

    def __str__(self):
        return self.nombre
