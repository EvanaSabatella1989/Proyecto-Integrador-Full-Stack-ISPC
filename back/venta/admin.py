from django.contrib import admin
from .models import Venta

# Register your models here.
class VentaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'cliente', 'tipo_pago', 'estado', 'total', 'fecha_pago')
    list_filter = ('estado', 'tipo_pago', 'fecha_pago')
    search_fields = ('numero_factura', 'cliente__user__email', 'cliente__user__first_name', 'cliente__user__last_name')
    date_hierarchy = 'fecha_pago'
    
    readonly_fields = ('numero_factura', 'fecha_pago')

    fieldsets = (
        ('Información de la venta', {
            'fields': ('numero_factura', 'cliente', 'total', 'tipo_pago', 'estado', 'fecha_pago')
        }),
    )
    

admin.site.register(Venta, VentaAdmin)