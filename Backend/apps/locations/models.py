from django.db import models
from math import radians, sin, cos, sqrt, atan2
from apps.users.models import Usuario


class Perimetro(models.Model):
    """Zona geográfica válida para registrar asistencia."""
    nombre = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    radio_metros = models.IntegerField(default=50)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Perímetro'
        verbose_name_plural = 'Perímetros'

    def __str__(self):
        return f"{self.nombre} (radio: {self.radio_metros}m)"

    def esta_dentro(self, lat, lng):
        """
        Calcula si un punto (lat, lng) está dentro del radio
        usando la fórmula de Haversine.
        Retorna (dentro: bool, distancia_metros: float)
        """
        R = 6371000  # Radio de la Tierra en metros

        lat1 = radians(float(self.latitud))
        lat2 = radians(float(lat))
        dlat = radians(float(lat) - float(self.latitud))
        dlng = radians(float(lng) - float(self.longitud))

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distancia = R * c
        return distancia <= self.radio_metros, round(distancia, 2)


class Asistencia(models.Model):
    """Registro de entrada o salida de un maestro."""

    class Tipo(models.TextChoices):
        ENTRADA = 'entrada', 'Entrada'
        SALIDA = 'salida', 'Salida'

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='asistencias')
    perimetro = models.ForeignKey(Perimetro, on_delete=models.CASCADE, related_name='asistencias')
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    latitud_real = models.DecimalField(max_digits=9, decimal_places=6)
    longitud_real = models.DecimalField(max_digits=9, decimal_places=6)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    valido = models.BooleanField(default=False)
    distancia_metros = models.FloatField(default=0, help_text='Distancia al centro del perímetro en metros')

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['-fecha_hora']

    def __str__(self):
        estado = "VÁLIDO" if self.valido else "INVÁLIDO"
        return f"{self.usuario.nombre} - {self.tipo} - {self.fecha_hora:%Y-%m-%d %H:%M} [{estado}]"


class Incidencia(models.Model):
    """Incidencias de asistencia: falta, retardo, justificación, etc."""

    class Tipo(models.TextChoices):
        FALTA = 'falta', 'Falta'
        RETARDO = 'retardo', 'Retardo'
        JUSTIFICACION = 'justificacion', 'Justificación'
        SALIDA_TEMPRANA = 'salida_temprana', 'Salida Temprana'

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='incidencias')
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Incidencia'
        verbose_name_plural = 'Incidencias'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.usuario.nombre} - {self.get_tipo_display()} - {self.fecha}"
