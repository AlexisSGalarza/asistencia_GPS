#!/usr/bin/env python
"""
Script de inicialización del sistema
Crea los roles básicos y un usuario administrador
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import Rol, Usuario

def inicializar_roles():
    """Crear los roles básicos del sistema"""
    roles = ['Administrador', 'Supervisor', 'Maestro']
    
    for nombre_rol in roles:
        rol, created = Rol.objects.get_or_create(nombre=nombre_rol)
        if created:
            print(f'✓ Rol creado: {nombre_rol}')
        else:
            print(f'- Rol ya existe: {nombre_rol}')

def crear_admin():
    """Crear un usuario administrador por defecto"""
    try:
        rol_admin = Rol.objects.get(nombre='Administrador')
        
        # Verificar si ya existe
        if Usuario.objects.filter(correo='admin@asistencia.com').exists():
            print(f'- Usuario administrador ya existe')
            return
        
        # Crear nuevo usuario
        admin = Usuario(
            correo='admin@asistencia.com',
            nombre='Administrador del Sistema',
            rol=rol_admin,
            activo=True
        )
        admin.set_password('admin123')  # Contraseña hasheada
        admin.save()
        
        print(f'✓ Usuario administrador creado')
        print(f'  Correo: admin@asistencia.com')
        print(f'  Password: admin123')
        print(f'\n⚠️  ⚠️  ADVERTENCIA DE SEGURIDAD ⚠️  ⚠️')
        print(f'  Esta es una contraseña DÉBIL de demostración')
        print(f'  DEBE cambiarla inmediatamente por una contraseña segura')
        print(f'  Nunca use contraseñas simples en producción')
        print(f'  Recomendado: 12+ caracteres con mayúsculas, minúsculas, números y símbolos')
            
    except Rol.DoesNotExist:
        print('✗ Error: Debes crear los roles primero')

if __name__ == '__main__':
    print('=== Inicializando Sistema de Asistencia GPS ===\n')
    
    print('1. Creando roles...')
    inicializar_roles()
    
    print('\n2. Creando usuario administrador...')
    crear_admin()
    
    print('\n=== Inicialización Completada ===')
