from django.contrib import admin
from .models import Reserva


class ReservaAdmin(admin.ModelAdmin):
    list_display = ('sucursal','servicio','hora_sucursal','fecha_sucursal','nombre_cliente','correo_cliente')
    list_display_links =  ('sucursal','servicio','hora_sucursal','fecha_sucursal','nombre_cliente','correo_cliente')
    search_fields = ('sucursal','servicio','hora_sucursal','fecha_sucursal','nombre_cliente','correo_cliente')
    list_per_page = 25


admin.site.register(Reserva,ReservaAdmin)
# Register your models here.
