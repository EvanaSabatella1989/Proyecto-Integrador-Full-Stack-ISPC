from django.contrib import admin
from .models import Turno
# Register your models here.


class TurnoAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'sucursal','fecha','hora','disponible')
    list_display_links = ('servicio', 'sucursal','fecha','hora','disponible')
    search_fields = ('servicio', 'sucursal','fecha','hora','disponible')
    list_per_page = 25


admin.site.register(Turno, TurnoAdmin)
