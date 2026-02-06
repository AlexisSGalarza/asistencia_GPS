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
        """Crea un usuario con contraseña hasheada"""
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def update(self, instance, validated_data):
        """Actualiza un usuario, hasheando la contraseña si se proporciona"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

class HorarioSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    
    class Meta:
        model = Horario
        fields = ['id', 'usuario', 'usuario_nombre', 'dia_semana', 'hora_entrada', 'hora_salida']
