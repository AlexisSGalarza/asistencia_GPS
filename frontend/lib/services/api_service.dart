import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Servicio centralizado para comunicarse con el backend Django.
class ApiService {
  // Para emulador Android usa 10.0.2.2, para iOS/desktop usa localhost
  static const String _baseUrl = 'http://10.0.2.2:8000/api';

  static String? _accessToken;
  static String? _refreshToken;
  static Map<String, dynamic>? _usuarioData;

  static const _storage = FlutterSecureStorage();

  // ─── Getters ───
  static String? get accessToken => _accessToken;
  static Map<String, dynamic>? get usuario => _usuarioData;
  static String get nombreUsuario => _usuarioData?['nombre'] ?? '';
  static String get correoUsuario => _usuarioData?['correo'] ?? '';
  static String get rolUsuario => _usuarioData?['rol_nombre'] ?? '';
  static String get creadoEn => _usuarioData?['created_at'] ?? '';
  static List<dynamic> get horarios => _usuarioData?['horarios'] ?? [];
  static bool get isAuthenticated => _accessToken != null;

  // ─── Headers ───
  static Map<String, String> get _headers => {
    'Content-Type': 'application/json',
  };

  static Map<String, String> get _authHeaders => {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer $_accessToken',
  };

  // ─── SECURE STORAGE ───

  /// Guarda tokens de forma segura (Keychain/Keystore).
  static Future<void> _guardarTokens() async {
    if (_accessToken != null) {
      await _storage.write(key: 'access_token', value: _accessToken);
    }
    if (_refreshToken != null) {
      await _storage.write(key: 'refresh_token', value: _refreshToken);
    }
    if (_usuarioData != null) {
      await _storage.write(
        key: 'usuario_data',
        value: jsonEncode(_usuarioData),
      );
    }
  }

  /// Intenta restaurar sesión desde almacenamiento seguro.
  static Future<bool> restaurarSesion() async {
    try {
      _accessToken = await _storage.read(key: 'access_token');
      _refreshToken = await _storage.read(key: 'refresh_token');
      final userData = await _storage.read(key: 'usuario_data');
      if (userData != null) {
        _usuarioData = jsonDecode(userData);
      }

      if (_accessToken != null) {
        // Verificar que el token sigue siendo válido
        final response = await http.get(
          Uri.parse('$_baseUrl/auth/perfil/'),
          headers: _authHeaders,
        );
        if (response.statusCode == 200) {
          _usuarioData = jsonDecode(response.body);
          return true;
        }
        // Token expirado, intentar refresh
        if (_refreshToken != null) {
          final refreshed = await refreshAccessToken();
          if (refreshed) {
            await _guardarTokens();
            return true;
          }
        }
      }
    } catch (_) {}

    // No se pudo restaurar
    await _limpiarStorage();
    return false;
  }

  static Future<void> _limpiarStorage() async {
    await _storage.deleteAll();
    _accessToken = null;
    _refreshToken = null;
    _usuarioData = null;
  }

  // ─── AUTH ───

  /// Login: envía correo y password, guarda tokens y datos del usuario.
  static Future<Map<String, dynamic>> login(
    String correo,
    String password,
  ) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/auth/login/'),
      headers: _headers,
      body: jsonEncode({'correo': correo, 'password': password}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      _accessToken = data['tokens']['access'];
      _refreshToken = data['tokens']['refresh'];
      _usuarioData = data['usuario'];
      await _guardarTokens();
      return {'success': true, 'data': data};
    } else {
      final error = jsonDecode(response.body);
      String mensaje = 'Error al iniciar sesión';
      if (error is Map) {
        if (error.containsKey('non_field_errors')) {
          mensaje = (error['non_field_errors'] as List).first;
        } else if (error.containsKey('detail')) {
          mensaje = error['detail'];
        }
      }
      return {'success': false, 'mensaje': mensaje};
    }
  }

  /// Refresh token: obtiene un nuevo access token.
  static Future<bool> refreshAccessToken() async {
    if (_refreshToken == null) return false;

    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/auth/refresh/'),
        headers: _headers,
        body: jsonEncode({'refresh': _refreshToken}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _accessToken = data['access'];
        await _guardarTokens();
        return true;
      }
    } catch (_) {}
    return false;
  }

  /// Logout: limpia tokens y datos del almacenamiento seguro.
  static Future<void> logout() async {
    await _limpiarStorage();
  }

  // ─── RECUPERACIÓN DE CONTRASEÑA ───

  /// Solicitar código de recuperación.
  static Future<Map<String, dynamic>> solicitarRecuperacion(
    String correo,
  ) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/auth/recuperar/solicitar/'),
      headers: _headers,
      body: jsonEncode({'correo': correo}),
    );

    final data = jsonDecode(response.body);
    if (response.statusCode == 200) {
      return {
        'success': true,
        'mensaje': data['mensaje'],
        'codigo_debug': data['codigo_debug'], // Solo en desarrollo
      };
    } else {
      return {
        'success': false,
        'mensaje': data['error'] ?? 'Error al solicitar recuperación',
      };
    }
  }

  /// Confirmar recuperación con código y nueva contraseña.
  static Future<Map<String, dynamic>> confirmarRecuperacion(
    String correo,
    String codigo,
    String nuevaPassword,
  ) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/auth/recuperar/confirmar/'),
      headers: _headers,
      body: jsonEncode({
        'correo': correo,
        'codigo': codigo,
        'nueva_password': nuevaPassword,
      }),
    );

    final data = jsonDecode(response.body);
    if (response.statusCode == 200) {
      return {'success': true, 'mensaje': data['mensaje']};
    } else {
      return {
        'success': false,
        'mensaje': data['error'] ?? 'Error al confirmar recuperación',
      };
    }
  }

  // ─── PERFIL ───

  /// Obtener perfil del usuario autenticado.
  static Future<Map<String, dynamic>> getPerfil() async {
    final response = await _getAuth('/auth/perfil/');
    if (response != null) {
      _usuarioData = response;
    }
    return response ?? {};
  }

  /// Cambiar contraseña.
  static Future<Map<String, dynamic>> cambiarPassword(
    String passwordActual,
    String passwordNuevo,
  ) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/auth/cambiar-password/'),
      headers: _authHeaders,
      body: jsonEncode({
        'password_actual': passwordActual,
        'password_nuevo': passwordNuevo,
      }),
    );

    if (response.statusCode == 200) {
      return {
        'success': true,
        'mensaje': 'Contraseña actualizada correctamente',
      };
    } else {
      final error = jsonDecode(response.body);
      String mensaje = 'Error al cambiar contraseña';
      if (error is Map && error.containsKey('password_actual')) {
        mensaje = (error['password_actual'] as List).first;
      }
      return {'success': false, 'mensaje': mensaje};
    }
  }

  // ─── HORARIOS ───

  /// Obtener horarios del maestro autenticado.
  static Future<List<dynamic>> getHorarios() async {
    final response = await _getAuth('/horarios/');
    if (response != null && response.containsKey('results')) {
      return response['results'] as List;
    }
    if (response != null) {
      return response['results'] ?? [];
    }
    return [];
  }

  // ─── ASISTENCIA ───

  /// Obtener el estado de asistencia de hoy (entrada/salida registradas).
  /// También activa auto-salida si pasaron +10h en el backend.
  static Future<Map<String, dynamic>> getEstadoHoy() async {
    final response = await _getAuth('/asistencia/estado-hoy/');
    if (response != null && response is Map<String, dynamic>) {
      return response;
    }
    return {
      'entrada_registrada': false,
      'salida_registrada': false,
    };
  }

  /// Registrar asistencia (entrada o salida) enviando lat/lng + ssid/bssid.
  static Future<Map<String, dynamic>> registrarAsistencia({
    required String tipo,
    required double latitud,
    required double longitud,
    String ssid = '',
    String bssid = '',
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/asistencia/registrar/'),
      headers: _authHeaders,
      body: jsonEncode({
        'tipo': tipo,
        'latitud': latitud,
        'longitud': longitud,
        'ssid': ssid,
        'bssid': bssid,
      }),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      return {'success': true, 'data': data};
    } else {
      final error = jsonDecode(response.body);
      String mensaje = 'Error al registrar asistencia';
      if (error is Map) {
        if (error.containsKey('non_field_errors')) {
          mensaje = (error['non_field_errors'] as List).first;
        } else if (error.containsKey('detail')) {
          mensaje = error['detail'];
        }
      }
      return {'success': false, 'mensaje': mensaje};
    }
  }

  /// Obtener historial de asistencia del maestro.
  static Future<List<dynamic>> getHistorial({
    String? fechaInicio,
    String? fechaFin,
  }) async {
    String url = '/asistencia/historial/';
    final params = <String>[];
    if (fechaInicio != null) params.add('fecha_inicio=$fechaInicio');
    if (fechaFin != null) params.add('fecha_fin=$fechaFin');
    if (params.isNotEmpty) url += '?${params.join('&')}';

    final response = await _getAuth(url);
    if (response is List) {
      return response;
    }
    return [];
  }

  // ─── INCIDENCIAS ───

  /// Obtener incidencias del maestro.
  static Future<List<dynamic>> getIncidencias() async {
    final response = await _getAuth('/asistencia/incidencias/');
    if (response != null && response.containsKey('results')) {
      return response['results'] as List;
    }
    return [];
  }

  // ─── REDES AUTORIZADAS ───

  /// Obtener lista de redes Wi-Fi autorizadas activas.
  static Future<List<dynamic>> getRedesActivas() async {
    final response = await _getAuth('/asistencia/redes-activas/');
    if (response is List) {
      return response;
    }
    return [];
  }

  // ─── HELPERS ───

  /// GET autenticado con manejo de refresh automático.
  static Future<dynamic> _getAuth(String path) async {
    var response = await http.get(
      Uri.parse('$_baseUrl$path'),
      headers: _authHeaders,
    );

    // Si el token expiró, intentar refresh
    if (response.statusCode == 401) {
      final refreshed = await refreshAccessToken();
      if (refreshed) {
        response = await http.get(
          Uri.parse('$_baseUrl$path'),
          headers: _authHeaders,
        );
      }
    }

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return null;
  }
}
