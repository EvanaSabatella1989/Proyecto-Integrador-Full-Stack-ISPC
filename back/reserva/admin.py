from django.contrib import admin
from .models import Reserva


class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente','turno','estado')
    list_display_links =   ('cliente','turno','estado')
    search_fields =  ('cliente','turno','estado')
    list_per_page = 25


admin.site.register(Reserva,ReservaAdmin)

