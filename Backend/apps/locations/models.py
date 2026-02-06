from django.db import models
# Importamos el modelo Usuario desde la otra carpeta (app)
from apps.users.models import Usuario

class Perimetro(models.Model):
    nombre = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    radio_metros = models.IntegerField(default=50)
    activo = models.BooleanField(default=True)

class Asistencia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    perimetro = models.ForeignKey(Perimetro, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10) # 'entrada' o 'salida'
    latitud_real = models.DecimalField(max_digits=9, decimal_places=6)
    longitud_real = models.DecimalField(max_digits=9, decimal_places=6)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    valido = models.BooleanField(default=False)
