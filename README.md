# 📍 Sistema de Asistencia GPS

Sistema completo de registro de asistencia basado en geolocalización para instituciones educativas. Permite que los maestros registren su entrada y salida solo cuando están dentro del perímetro de la escuela.

## 🎯 Descripción del Proyecto

Aplicación móvil multiplataforma (Android, iOS, Huawei) con backend Django que gestiona la asistencia del personal docente mediante validación GPS en tiempo real.

## ✨ Características Principales

- 📱 **Registro por GPS**: Validación automática de ubicación al registrar entrada/salida
- 👥 **Sistema de Roles**: Administrador, Supervisor y Maestro
- 📊 **Historial Completo**: Consulta de registros con filtros por fecha
- 📈 **Panel de Supervisión**: Dashboard en tiempo real para directivos
- ⚙️ **Gestión Administrativa**: Creación de usuarios, horarios y configuración de perímetros
- 📄 **Reportes**: Generación de reportes descargables en PDF
- 🔐 **Seguridad**: Autenticación JWT y contraseñas hasheadas

## 🏗️ Arquitectura

### Backend
- **Framework**: Django 6.0.2 + Django REST Framework
- **Base de Datos**: PostgreSQL
- **Autenticación**: JWT (Simple JWT)
- **Validación GPS**: Fórmula de Haversine

### Frontend (En desarrollo)
- **Framework**: Flutter (Dart)
- **Plataformas**: Android, iOS, Huawei AppGallery

## 🚀 Estado del Proyecto

### ✅ Completado (Backend)
- [x] API REST completa con 13+ endpoints
- [x] Sistema de autenticación con JWT
- [x] Validación GPS automática
- [x] CRUD de usuarios, roles, horarios y perímetros
- [x] Historial y reportes de asistencias
- [x] Panel de administración Django
- [x] Documentación completa

### 🔨 En Progreso
- [ ] Aplicación móvil Flutter
- [ ] Generación de PDFs
- [ ] Sistema de notificaciones
- [ ] Validación de horarios

## 📦 Instalación

### Requisitos Previos
- Python 3.8+
- PostgreSQL
- Flutter 3.0+ (para el frontend)

### Backend - Inicio Rápido

```bash
# 1. Clonar repositorio
git clone https://github.com/AlexisSGalarza/asistencia_GPS.git
cd asistencia_GPS/Backend

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp claves.env.example claves.env
# Editar claves.env con tus credenciales

# 4. Crear base de datos
createdb asistencia_gps

# 5. Aplicar migraciones
python manage.py migrate

# 6. Inicializar datos (roles y admin)
python inicializar.py

# 7. Iniciar servidor
python manage.py runserver 0.0.0.0:8000
```

**Usuario por defecto:**
- Email: `admin@asistencia.com`
- Password: `admin123`

## 📚 Documentación

- **[📖 README Backend](Backend/README.md)**: Documentación completa de la API
- **[⚡ Inicio Rápido](INICIO_RAPIDO.md)**: Setup en 5 minutos
- **[📊 Análisis Completo](ANALISIS_PROYECTO.md)**: Estado del proyecto y roadmap

## 🔌 API Endpoints

### Autenticación
```http
POST /api/users/usuarios/login/
POST /api/token/
POST /api/token/refresh/
```

### Usuarios y Roles
```http
GET/POST /api/users/usuarios/
GET /api/users/usuarios/maestros/
GET/POST /api/users/roles/
GET/POST /api/users/horarios/
```

### Asistencia y Perímetros
```http
POST /api/locations/asistencias/registrar/
GET /api/locations/asistencias/historial/
GET /api/locations/asistencias/hoy/
GET /api/locations/asistencias/reporte/
GET/POST /api/locations/perimetros/
```

Ver [documentación completa de endpoints](Backend/README.md#-documentación-de-la-api).

## 🧪 Ejemplo de Uso

### Registrar Asistencia
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

**Respuesta:**
```json
{
  "mensaje": "Asistencia (entrada) registrada correctamente",
  "asistencia": {
    "id": 1,
    "valido": true,
    "distancia_metros": 15.5,
    "fecha_hora": "2026-02-06T14:30:00Z"
  }
}
```

## 🗂️ Estructura del Proyecto

```
asistencia_GPS/
├── Backend/
│   ├── apps/
│   │   ├── users/          # Usuarios, roles, horarios
│   │   └── locations/      # Perímetros y asistencias
│   ├── config/             # Configuración Django
│   ├── requirements.txt
│   ├── inicializar.py      # Script de setup
│   └── README.md
├── ANALISIS_PROYECTO.md    # Análisis completo
├── INICIO_RAPIDO.md        # Guía rápida
└── README.md               # Este archivo
```

## 🔐 Seguridad

- ✅ Contraseñas hasheadas con PBKDF2
- ✅ Autenticación JWT con tokens de 8 horas
- ✅ CORS configurado
- ✅ Validación de datos en serializers
- ⚠️ **Importante**: Cambiar SECRET_KEY en producción

## 🤝 Contribución

Este es un proyecto privado de desarrollo. Para contribuir:

1. Crea un branch desde `main`
2. Realiza tus cambios
3. Envía un Pull Request

## 📝 Requerimientos Funcionales

1. ✅ **Registro por GPS**: Validación automática de perímetro
2. ✅ **Inicio de sesión y roles**: Sistema de autenticación completo
3. ✅ **Historial de asistencia**: Consulta con filtros
4. 🔨 **Panel de supervisión**: Dashboard en desarrollo
5. ✅ **Gestión administrativa**: CRUD completo de usuarios
6. ✅ **Configuración de perímetro GPS**: Gestión de zonas
7. 🔨 **Generación de reportes**: Endpoint listo, PDF pendiente
8. 🔨 **Compatibilidad multiplataforma**: Frontend en desarrollo

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Estado |
|------------|------------|--------|
| Backend API | Django + DRF | ✅ Completado |
| Base de Datos | PostgreSQL | ✅ Configurado |
| Autenticación | JWT | ✅ Implementado |
| Frontend Mobile | Flutter | 🔨 Pendiente |
| Reportes | ReportLab | 🔨 Por hacer |

## 📊 Progreso del Proyecto

- **Backend API**: 80% ✅
- **Seguridad**: 90% ✅
- **Documentación**: 100% ✅
- **Frontend Mobile**: 0% 🔨
- **Testing**: 10% ⚠️

## 🎯 Próximos Pasos

1. **Inmediato**: Desarrollar aplicación Flutter
2. **Corto plazo**: Implementar generación de PDFs
3. **Mediano plazo**: Sistema de notificaciones
4. **Largo plazo**: Dashboard web para administradores

## 📞 Soporte

Para problemas o preguntas:
- Ver [Problemas Comunes](INICIO_RAPIDO.md#-problemas-comunes)
- Revisar [Documentación Completa](Backend/README.md)
- Consultar [Análisis del Proyecto](ANALISIS_PROYECTO.md)

## 📄 Licencia

Este proyecto es privado y confidencial.

---

**Desarrollado con ❤️ para facilitar la gestión de asistencia educativa**
