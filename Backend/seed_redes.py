"""Seed script para crear redes Wi-Fi autorizadas de prueba."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.locations.models import RedAutorizada

redes = [
    {
        'nombre': 'Red Principal - Sala de Maestros',
        'ssid': 'ESCUELA_WIFI',
        'bssid': 'AA:BB:CC:DD:EE:01',
        'descripcion': 'Access point ubicado en la sala de maestros',
        'activo': True,
    },
    {
        'nombre': 'Red Secundaria - Direccion',
        'ssid': 'ESCUELA_WIFI',
        'bssid': 'AA:BB:CC:DD:EE:02',
        'descripcion': 'Access point ubicado en la direccion',
        'activo': True,
    },
    {
        'nombre': 'Red Biblioteca',
        'ssid': 'ESCUELA_BIBLIO',
        'bssid': 'AA:BB:CC:DD:EE:03',
        'descripcion': 'Access point de la biblioteca',
        'activo': True,
    },
    {
        'nombre': 'Red de Prueba Emulador',
        'ssid': 'AndroidWifi',
        'bssid': '02:15:B2:00:01:00',
        'descripcion': 'Red Wi-Fi del emulador Android (para desarrollo)',
        'activo': True,
    },
]

for red_data in redes:
    red, created = RedAutorizada.objects.get_or_create(
        ssid=red_data['ssid'],
        bssid=red_data['bssid'],
        defaults={
            'nombre': red_data['nombre'],
            'descripcion': red_data['descripcion'],
            'activo': red_data['activo'],
        }
    )
    if created:
        print(f'Red creada: {red.nombre} -- SSID: {red.ssid} | BSSID: {red.bssid}')
    else:
        print(f'Ya existe: {red.nombre}')

print(f'\nTotal redes autorizadas: {RedAutorizada.objects.count()}')
