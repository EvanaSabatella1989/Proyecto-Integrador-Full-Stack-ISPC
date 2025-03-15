from django.contrib import admin
from .models import Reserva


class ReservalAdmin(admin.ModelAdmin):
    list_display = ('sucursal','servicio','horario','nombre_cliente','correo_cliente')
    list_display_links =  ('sucursal','servicio','horario','nombre_cliente','correo_cliente')
    search_fields = ('sucursal','servicio','horario','nombre_cliente','correo_cliente')
    list_per_page = 25


admin.site.register(Reserva,ReservalAdmin)
# Register your models here.
