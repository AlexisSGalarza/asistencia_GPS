from django.contrib import admin
from .models import Perimetro, Asistencia

@admin.register(Perimetro)
class PerimetroAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'latitud', 'longitud', 'radio_metros', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'perimetro', 'tipo', 'fecha_hora', 'valido']
    list_filter = ['tipo', 'valido', 'fecha_hora']
    search_fields = ['usuario__nombre']
    date_hierarchy = 'fecha_hora'
