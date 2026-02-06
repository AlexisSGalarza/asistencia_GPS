from django.db import models
from django.contrib.auth.hashers import make_password, check_password as check_pwd


class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre} ({self.correo})"
    
    def set_password(self, raw_password):
        """Hashea y guarda la contraseña"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verifica si la contraseña es correcta"""
        return check_pwd(raw_password, self.password)

class Horario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    dia_semana = models.IntegerField() # 0=Dom, 1=Lun...
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    
    def __str__(self):
        dias = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
        return f"{self.usuario.nombre} - {dias[self.dia_semana]}"
    
    class Meta:
        verbose_name_plural = "Horarios"
