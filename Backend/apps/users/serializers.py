from rest_framework import serializers
from .models import Rol, Usuario, Horario

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre']

class UsuarioSerializer(serializers.ModelSerializer):
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'correo', 'password', 'activo', 'rol', 'rol_nombre']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        # Hash de la contraseña antes de guardar
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        # Aquí deberías usar un hash real en producción (ej: bcrypt)
        usuario.password = password
        usuario.save()
        return usuario

class HorarioSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    
    class Meta:
        model = Horario
        fields = ['id', 'usuario', 'usuario_nombre', 'dia_semana', 'hora_entrada', 'hora_salida']
