# 🎯 Guía de Uso Completa - Sistema de Asistencia GPS

## 📖 LÉEME PRIMERO

Este documento te guía paso a paso para usar tu sistema completo.

---

## 🚀 PASO 1: Configurar el Backend (10 minutos)

### 1.1. Instalar dependencias
```bash
cd Backend
pip install -r requirements.txt
```

### 1.2. Configurar base de datos
```bash
# Crear archivo de configuración
cp claves.env.example claves.env

# Editar con tus datos (nano, vim, o tu editor favorito)
nano claves.env
```

Contenido de `claves.env`:
```
SECRET_KEY=tu-clave-secreta-random-aqui
DEBUG=True
DB_NAME=asistencia_gps
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_password_postgres
DB_HOST=localhost
DB_PORT=5432
```

### 1.3. Crear base de datos en PostgreSQL
```bash
# Conectarse a PostgreSQL
psql -U postgres

# Crear la base de datos
CREATE DATABASE asistencia_gps;

# Salir
\q
```

### 1.4. Aplicar migraciones
```bash
python manage.py migrate
```

### 1.5. Inicializar datos
```bash
python inicializar.py
```

Esto creará:
- ✅ Rol "Administrador"
- ✅ Rol "Supervisor"
- ✅ Rol "Maestro"
- ✅ Usuario admin (admin@asistencia.com / admin123)

### 1.6. Iniciar servidor
```bash
python manage.py runserver 0.0.0.0:8000
```

✅ **Backend funcionando en: http://localhost:8000**

---

## 🧪 PASO 2: Probar la API (15 minutos)

### 2.1. Panel de Administración

Visita: http://localhost:8000/admin/

Crear superusuario:
```bash
python manage.py createsuperuser
```

### 2.2. Probar endpoints con curl

#### Login
```bash
curl -X POST http://localhost:8000/api/users/usuarios/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "correo": "admin@asistencia.com",
    "password": "admin123"
  }'
```

**Respuesta:**
```json
{
  "mensaje": "Login exitoso",
  "usuario": {
    "id": 1,
    "nombre": "Administrador del Sistema",
    "correo": "admin@asistencia.com",
    "rol": 1,
    "rol_nombre": "Administrador"
  }
}
```

#### Crear un perímetro GPS
```bash
curl -X POST http://localhost:8000/api/locations/perimetros/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Escuela Primaria Central",
    "latitud": "19.432608",
    "longitud": "-99.133209",
    "radio_metros": 100,
    "activo": true
  }'
```

#### Crear un maestro
```bash
curl -X POST http://localhost:8000/api/users/usuarios/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "correo": "juan@escuela.com",
    "password": "maestro123",
    "rol": 3,
    "activo": true
  }'
```

#### Registrar asistencia (entrada)
```bash
curl -X POST http://localhost:8000/api/locations/asistencias/registrar/ \
  -H "Content-Type: application/json" \
  -d '{
    "usuario": 2,
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
    "usuario": 2,
    "usuario_nombre": "Juan Pérez",
    "perimetro": 1,
    "perimetro_nombre": "Escuela Primaria Central",
    "tipo": "entrada",
    "valido": true,
    "distancia_metros": 15.5,
    "fecha_hora": "2026-02-06T14:30:00Z"
  }
}
```

#### Consultar historial
```bash
curl "http://localhost:8000/api/locations/asistencias/historial/?usuario_id=2"
```

### 2.3. Probar con Postman

1. Importa esta colección en Postman
2. Configura la URL base: `http://localhost:8000/api`
3. Prueba todos los endpoints

---

## 📱 PASO 3: Desarrollar Frontend Flutter (Siguiente fase)

### 3.1. Crear proyecto Flutter
```bash
flutter create asistencia_gps_app
cd asistencia_gps_app
```

### 3.2. Agregar dependencias en `pubspec.yaml`
```yaml
dependencies:
  http: ^1.1.0
  geolocator: ^10.1.0
  flutter_secure_storage: ^9.0.0
  provider: ^6.1.0
```

### 3.3. Estructura recomendada
```
lib/
  ├── main.dart
  ├── models/
  │   ├── usuario.dart
  │   ├── asistencia.dart
  │   └── perimetro.dart
  ├── services/
  │   ├── api_service.dart
  │   ├── auth_service.dart
  │   └── gps_service.dart
  ├── screens/
  │   ├── login_screen.dart
  │   ├── home_screen.dart
  │   ├── registro_asistencia_screen.dart
  │   └── historial_screen.dart
  └── widgets/
      └── ...
```

### 3.4. Ejemplo: Login en Flutter

```dart
// services/api_service.dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api';
  
  Future<Map<String, dynamic>> login(String correo, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/users/usuarios/login/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'correo': correo,
        'password': password,
      }),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Login fallido');
    }
  }
}
```

### 3.5. Ejemplo: Obtener ubicación GPS

```dart
// services/gps_service.dart
import 'package:geolocator/geolocator.dart';

class GpsService {
  Future<Position> obtenerUbicacionActual() async {
    // Verificar permisos
    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }
    
    // Obtener ubicación
    return await Geolocator.getCurrentPosition(
      desiredAccuracy: LocationAccuracy.high
    );
  }
  
  double calcularDistancia(double lat1, double lon1, double lat2, double lon2) {
    return Geolocator.distanceBetween(lat1, lon1, lat2, lon2);
  }
}
```

### 3.6. Ejemplo: Registrar asistencia

```dart
Future<void> registrarAsistencia() async {
  // 1. Obtener ubicación actual
  Position posicion = await GpsService().obtenerUbicacionActual();
  
  // 2. Enviar a API
  final response = await http.post(
    Uri.parse('$baseUrl/locations/asistencias/registrar/'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode({
      'usuario': usuarioId,
      'perimetro': perimetroId,
      'tipo': 'entrada',
      'latitud_real': posicion.latitude.toString(),
      'longitud_real': posicion.longitude.toString(),
    }),
  );
  
  // 3. Mostrar resultado
  if (response.statusCode == 201) {
    final data = json.decode(response.body);
    if (data['asistencia']['valido']) {
      mostrarMensaje('¡Asistencia registrada exitosamente!');
    } else {
      mostrarMensaje('Estás fuera del perímetro permitido');
    }
  }
}
```

---

## 📊 PASO 4: Entender los Roles

### Administrador
**Permisos:**
- ✅ Crear/editar/eliminar usuarios
- ✅ Configurar perímetros GPS
- ✅ Gestionar horarios
- ✅ Ver todos los reportes
- ✅ Acceso completo al sistema

**Pantallas Flutter:**
- Dashboard admin
- Gestión de usuarios
- Configuración de perímetros
- Reportes completos

### Supervisor
**Permisos:**
- ✅ Ver asistencias de todos
- ✅ Generar reportes
- ❌ No puede editar configuración

**Pantallas Flutter:**
- Dashboard supervisor
- Lista de asistencias en tiempo real
- Reportes por período
- Estadísticas

### Maestro
**Permisos:**
- ✅ Registrar su propia asistencia
- ✅ Ver su historial personal
- ❌ No puede ver datos de otros

**Pantallas Flutter:**
- Botón grande de registro
- Historial personal
- Perfil

---

## 🎯 PASO 5: Flujo de Uso Normal

### Configuración Inicial (Una vez)
1. Admin crea perímetro GPS de la escuela
2. Admin crea usuarios (maestros)
3. Admin configura horarios

### Uso Diario (Maestros)
1. Maestro abre app
2. Hace login
3. Click en "Registrar Entrada"
4. App lee GPS automáticamente
5. Envía a API
6. Muestra resultado (✅ dentro o ❌ fuera)
7. Al salir: "Registrar Salida"

### Supervisión (Supervisor/Admin)
1. Login en app
2. Ve dashboard con asistencias del día
3. Puede filtrar por fecha
4. Genera reportes

---

## 🔍 PASO 6: Debugging

### Verificar que backend funciona
```bash
# Ver logs del servidor
python manage.py runserver

# Ver en consola las peticiones HTTP
```

### Verificar base de datos
```bash
# Conectar a PostgreSQL
psql -U postgres -d asistencia_gps

# Ver usuarios
SELECT * FROM users_usuario;

# Ver asistencias
SELECT * FROM locations_asistencia;
```

### Ver admin panel
http://localhost:8000/admin/

---

## 📚 PASO 7: Documentación Adicional

Para más detalles, lee estos archivos en orden:

1. **RESPUESTA_FINAL.md** ⭐ - Análisis completo de qué tienes
2. **INICIO_RAPIDO.md** - Setup rápido del backend
3. **Backend/README.md** - Documentación detallada API
4. **ANALISIS_PROYECTO.md** - Roadmap completo
5. **RESUMEN.md** - Resumen ejecutivo

---

## ⚠️ IMPORTANTE ANTES DE PRODUCCIÓN

### Seguridad
1. Cambiar `SECRET_KEY` en `claves.env`
2. Cambiar contraseña de admin
3. Configurar `CORS_ALLOWED_ORIGINS` específicos
4. Habilitar HTTPS
5. Usar contraseñas fuertes

### Base de Datos
1. Configurar backups automáticos
2. Optimizar índices
3. Monitorear performance

### Servidor
1. Usar gunicorn + nginx
2. Configurar logs
3. Monitoring (Sentry, etc.)

---

## 💡 TIPS

### Para desarrollo
- Usa el panel admin para crear datos de prueba
- Postman para probar endpoints
- Logs del servidor para debugging

### Para producción
- Documentar todo cambio
- Hacer backups antes de cambios
- Testing exhaustivo
- Deploy gradual

---

## ✅ CHECKLIST DE INICIO

- [ ] Backend instalado y funcionando
- [ ] Base de datos creada y migrada
- [ ] Usuario admin creado
- [ ] Perímetro de prueba creado
- [ ] API testeada con curl/Postman
- [ ] Panel admin accesible
- [ ] Documentación leída
- [ ] Proyecto Flutter creado
- [ ] Primer endpoint integrado en Flutter

---

**¡Todo listo para comenzar! Si tienes dudas, revisa la documentación o consulta los ejemplos.** 🚀
