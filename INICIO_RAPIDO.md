# 🚀 Guía de Inicio Rápido - Sistema de Asistencia GPS

## ⚡ Setup en 5 minutos

### 1. Instalar Dependencias
```bash
cd Backend
pip install -r requirements.txt
```

### 2. Configurar Base de Datos
Edita `claves.env` con tus credenciales:
```bash
cp claves.env.example claves.env
nano claves.env
```

### 3. Crear Base de Datos
```sql
-- En PostgreSQL:
CREATE DATABASE asistencia_gps;
```

### 4. Aplicar Migraciones
```bash
python manage.py migrate
```

### 5. Inicializar Datos
```bash
python inicializar.py
```
Esto crea:
- Roles: Administrador, Supervisor, Maestro
- Usuario admin: `admin@asistencia.com` / `admin123`

### 6. Iniciar Servidor
```bash
python manage.py runserver 0.0.0.0:8000
```

## 🧪 Probar la API

### 1. Login
```bash
curl -X POST http://localhost:8000/api/users/usuarios/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "correo": "admin@asistencia.com",
    "password": "admin123"
  }'
```

### 2. Crear Perímetro
```bash
curl -X POST http://localhost:8000/api/locations/perimetros/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "nombre": "Escuela Central",
    "latitud": "19.432608",
    "longitud": "-99.133209",
    "radio_metros": 100,
    "activo": true
  }'
```

### 3. Registrar Asistencia
```bash
curl -X POST http://localhost:8000/api/locations/asistencias/registrar/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "usuario": 1,
    "perimetro": 1,
    "tipo": "entrada",
    "latitud_real": "19.432500",
    "longitud_real": "-99.133100"
  }'
```

## 📱 Panel de Administración

Visita: http://localhost:8000/admin/

Crea un superusuario:
```bash
python manage.py createsuperuser
```

## 📋 Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/users/usuarios/login/` | POST | Login |
| `/api/users/usuarios/` | GET/POST | Gestión de usuarios |
| `/api/users/roles/` | GET | Listar roles |
| `/api/users/horarios/` | GET/POST | Gestión de horarios |
| `/api/locations/perimetros/` | GET/POST | Gestión de perímetros |
| `/api/locations/asistencias/registrar/` | POST | Registrar asistencia |
| `/api/locations/asistencias/historial/` | GET | Historial |

## ❓ Problemas Comunes

### Error: "connection refused" PostgreSQL
```bash
# Verificar que PostgreSQL está corriendo:
sudo systemctl status postgresql
sudo systemctl start postgresql
```

### Error: "SECRET_KEY environment variable"
```bash
# Asegúrate de tener el archivo claves.env con SECRET_KEY
cp claves.env.example claves.env
```

### Error: migraciones pendientes
```bash
python manage.py migrate
```

## 📖 Documentación Completa

- **README Backend:** `Backend/README.md`
- **Análisis Completo:** `ANALISIS_PROYECTO.md`
- **API Docs:** Ver README para ejemplos detallados

## 🎯 Siguiente Paso

**¡Crear la app móvil en Flutter!**

El backend está listo y funcionando. Ahora necesitas desarrollar la interfaz móvil que consuma esta API.
