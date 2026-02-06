from django.db import models


class Rol(models.Model):
    nombre = models.CharField(max_length=50)

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

class Horario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    dia_semana = models.IntegerField() # 0=Dom, 1=Lun...
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
# Create your models here.
