from django.contrib import admin

from reservas_hotel.models import Usuario, Historial

class usuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']

admin.site.register(Usuario, usuarioAdmin)

class historialAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'descripcion', 'tabla_afectada', 'fecha']
admin.site.register(Historial, historialAdmin)