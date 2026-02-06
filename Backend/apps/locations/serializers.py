from rest_framework import serializers
from .models import Perimetro, Asistencia
from math import radians, cos, sin, asin, sqrt

class PerimetroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perimetro
        fields = ['id', 'nombre', 'latitud', 'longitud', 'radio_metros', 'activo']

class AsistenciaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    perimetro_nombre = serializers.CharField(source='perimetro.nombre', read_only=True)
    distancia_metros = serializers.SerializerMethodField()
    
    class Meta:
        model = Asistencia
        fields = ['id', 'usuario', 'usuario_nombre', 'perimetro', 'perimetro_nombre', 
                  'tipo', 'latitud_real', 'longitud_real', 'fecha_hora', 'valido', 'distancia_metros']
        read_only_fields = ['valido', 'fecha_hora']
    
    def get_distancia_metros(self, obj):
        """Calcula la distancia entre el punto real y el perímetro"""
        return self.calcular_distancia(
            float(obj.perimetro.latitud), 
            float(obj.perimetro.longitud),
            float(obj.latitud_real), 
            float(obj.longitud_real)
        )
    
    @staticmethod
    def calcular_distancia(lat1, lon1, lat2, lon2):
        """
        Calcula la distancia en metros entre dos puntos GPS usando la fórmula de Haversine
        """
        # Convertir grados a radianes
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Diferencias
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        # Fórmula de Haversine
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        # Radio de la Tierra en metros
        r = 6371000
        
        return c * r
    
    def create(self, validated_data):
        """Valida automáticamente si la asistencia está dentro del perímetro"""
        perimetro = validated_data['perimetro']
        lat_real = float(validated_data['latitud_real'])
        lon_real = float(validated_data['longitud_real'])
        
        # Calcular distancia
        distancia = self.calcular_distancia(
            float(perimetro.latitud),
            float(perimetro.longitud),
            lat_real,
            lon_real
        )
        
        # Validar si está dentro del radio permitido
        validated_data['valido'] = distancia <= perimetro.radio_metros
        
        return super().create(validated_data)
