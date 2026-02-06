# Sistema de Asistencia GPS - Backend

Backend desarrollado con Django y Django REST Framework para el sistema de asistencia GPS.

## 🚀 Características

- ✅ API REST completa
- ✅ Autenticación con JWT
- ✅ Validación de ubicación GPS automática
- ✅ Gestión de usuarios y roles
- ✅ Registro de asistencias (entrada/salida)
- ✅ Historial de asistencias
- ✅ Generación de reportes
- ✅ Panel de administración Django

## 📋 Requisitos

- Python 3.8+
- PostgreSQL
- pip

## 🔧 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar base de datos

Crea un archivo `claves.env` basado en `claves.env.example`:

```bash
cp claves.env.example claves.env
```

Edita `claves.env` con tus credenciales de PostgreSQL:

```
DB_NAME=asistencia_gps
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
```

### 3. Crear base de datos en PostgreSQL

```sql
CREATE DATABASE asistencia_gps;
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Inicializar datos (roles y admin)

```bash
python inicializar.py
```

Esto creará:
- Los roles: Administrador, Supervisor, Maestro
- Usuario admin por defecto:
  - Correo: `admin@asistencia.com`
  - Password: `admin123`

### 6. Crear superusuario Django (opcional)

```bash
python manage.py createsuperuser
```

### 7. Iniciar servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

## 📚 Documentación de la API

### Base URL
```
http://localhost:8000/api/
```

### Autenticación

La API usa JWT (JSON Web Tokens). La mayoría de endpoints requieren autenticación.

#### Obtener Token
```http
POST /api/token/
Content-Type: application/json

{
  "correo": "admin@asistencia.com",
  "password": "admin123"
}
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Para usar el token, incluye en el header:
```
Authorization: Bearer <access_token>
```

### Endpoints de Usuarios

#### Login Simple
```http
POST /api/users/usuarios/login/
Content-Type: application/json

{
  "correo": "maestro@escuela.com",
  "password": "password123"
}
```

#### Listar Usuarios
```http
GET /api/users/usuarios/
Authorization: Bearer <token>
```

#### Crear Usuario
```http
POST /api/users/usuarios/
Authorization: Bearer <token>
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "correo": "juan@escuela.com",
  "password": "password123",
  "rol": 1,
  "activo": true
}
```

#### Listar Maestros
```http
GET /api/users/usuarios/maestros/
Authorization: Bearer <token>
```

### Endpoints de Roles

#### Listar Roles
```http
GET /api/users/roles/
Authorization: Bearer <token>
```

**Respuesta:**
```json
[
  {"id": 1, "nombre": "Administrador"},
  {"id": 2, "nombre": "Supervisor"},
  {"id": 3, "nombre": "Maestro"}
]
```

### Endpoints de Horarios

#### Listar Horarios
```http
GET /api/users/horarios/
Authorization: Bearer <token>
```

#### Crear Horario
```http
POST /api/users/horarios/
Authorization: Bearer <token>
Content-Type: application/json

{
  "usuario": 1,
  "dia_semana": 1,
  "hora_entrada": "08:00:00",
  "hora_salida": "14:00:00"
}
```

Donde `dia_semana`: 0=Domingo, 1=Lunes, ..., 6=Sábado

#### Obtener Mis Horarios
```http
GET /api/users/horarios/mis_horarios/?usuario_id=1
Authorization: Bearer <token>
```

### Endpoints de Perímetros

#### Listar Perímetros
```http
GET /api/locations/perimetros/
Authorization: Bearer <token>
```

#### Crear Perímetro
```http
POST /api/locations/perimetros/
Authorization: Bearer <token>
Content-Type: application/json

{
  "nombre": "Escuela Primaria Central",
  "latitud": "19.432608",
  "longitud": "-99.133209",
  "radio_metros": 100,
  "activo": true
}
```

#### Perímetros Activos
```http
GET /api/locations/perimetros/activos/
Authorization: Bearer <token>
```

### Endpoints de Asistencia

#### Registrar Asistencia (Entrada/Salida)
```http
POST /api/locations/asistencias/registrar/
Authorization: Bearer <token>
Content-Type: application/json

{
  "usuario": 1,
  "perimetro": 1,
  "tipo": "entrada",
  "latitud_real": "19.432500",
  "longitud_real": "-99.133100"
}
```

**Nota:** El sistema valida automáticamente si la ubicación está dentro del perímetro usando la fórmula de Haversine.

**Respuesta:**
```json
{
  "mensaje": "Asistencia (entrada) registrada correctamente",
  "asistencia": {
    "id": 1,
    "usuario": 1,
    "usuario_nombre": "Juan Pérez",
    "perimetro": 1,
    "perimetro_nombre": "Escuela Primaria Central",
    "tipo": "entrada",
    "latitud_real": "19.432500",
    "longitud_real": "-99.133100",
    "fecha_hora": "2026-02-06T14:30:00Z",
    "valido": true,
    "distancia_metros": 15.5
  }
}
```

#### Historial de Asistencia
```http
GET /api/locations/asistencias/historial/?usuario_id=1&fecha_inicio=2026-02-01&fecha_fin=2026-02-28
Authorization: Bearer <token>
```

#### Asistencias de Hoy
```http
GET /api/locations/asistencias/hoy/?usuario_id=1
Authorization: Bearer <token>
```

#### Generar Reporte
```http
GET /api/locations/asistencias/reporte/?fecha_inicio=2026-02-01&fecha_fin=2026-02-28
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "fecha_inicio": "2026-02-01",
  "fecha_fin": "2026-02-28",
  "datos": [
    {
      "usuario": "Juan Pérez",
      "correo": "juan@escuela.com",
      "total_registros": 40,
      "registros_validos": 38,
      "registros_invalidos": 2
    }
  ]
}
```

## 🔐 Panel de Administración

Accede al panel de administración Django:

```
http://localhost:8000/admin/
```

Desde ahí puedes:
- Gestionar usuarios, roles y horarios
- Ver y editar perímetros
- Revisar todas las asistencias
- Administrar toda la base de datos

## 🧪 Validación GPS

El sistema calcula automáticamente:
1. La distancia entre la ubicación real y el centro del perímetro
2. Valida si está dentro del radio permitido
3. Marca la asistencia como válida o inválida

Formula utilizada: **Haversine** (precisión hasta metros)

## 📊 Modelos de Datos

### Usuario
- nombre
- correo (único)
- password
- activo (bool)
- rol (FK a Rol)

### Rol
- nombre (Administrador, Supervisor, Maestro)

### Horario
- usuario (FK)
- dia_semana (0-6)
- hora_entrada
- hora_salida

### Perímetro
- nombre
- latitud
- longitud
- radio_metros
- activo (bool)

### Asistencia
- usuario (FK)
- perimetro (FK)
- tipo (entrada/salida)
- latitud_real
- longitud_real
- fecha_hora (auto)
- valido (bool, calculado automáticamente)

## 🎯 Próximos Pasos

Para completar el sistema:

1. **Seguridad:**
   - Implementar hash de contraseñas (bcrypt)
   - Configurar permisos por rol
   - Configurar CORS para producción

2. **Frontend Flutter:**
   - Crear aplicación móvil
   - Integrar con la API
   - Implementar lectura de GPS
   - Solicitar permisos de ubicación

3. **Funcionalidades Avanzadas:**
   - Generación de PDFs
   - Notificaciones push
   - Manejo de incidencias
   - Dashboard de estadísticas

## 📝 Licencia

Este proyecto es privado y confidencial.
