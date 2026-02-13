import 'dart:async';
import 'package:flutter/material.dart';
import '../login/login_screen.dart';

class MarcarAsistenciaScreen extends StatefulWidget {
  const MarcarAsistenciaScreen({super.key});

  @override
  State<MarcarAsistenciaScreen> createState() => _MarcarAsistenciaScreenState();
}

class _MarcarAsistenciaScreenState extends State<MarcarAsistenciaScreen> {
  bool _dentroDelPerimetro = true;
  bool _entradaRegistrada = false;
  bool _salidaRegistrada = false;
  String _horaActual = '';
  String _fechaActual = '';
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _actualizarReloj();
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      _actualizarReloj();
    });
  }

  void _actualizarReloj() {
    final now = DateTime.now();
    setState(() {
      _horaActual =
          '${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}:${now.second.toString().padLeft(2, '0')}';
      final meses = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
      ];
      final dias = [
        'Lunes', 'Martes', 'Miércoles', 'Jueves',
        'Viernes', 'Sábado', 'Domingo'
      ];
      _fechaActual =
          '${dias[now.weekday - 1]}, ${now.day} de ${meses[now.month - 1]} ${now.year}';
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Scaffold(
      backgroundColor: const Color(0xFFF1E9F8),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Column(
            children: [
              _buildHeader(size),
              const SizedBox(height: 15),
              _buildMapaBlob(size),
              const SizedBox(height: 20),
              _buildFechaHora(),
              const SizedBox(height: 15),
              _buildEstado(),
              const SizedBox(height: 20),
              _buildBotones(size),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
      bottomNavigationBar: _buildBottomNav(),
    );
  }

  // ---------- Encabezado ----------
  Widget _buildHeader(Size size) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 25, vertical: 10),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: const [
              Text(
                'Hello!',
                style: TextStyle(
                  fontFamily: 'Merriweather',
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF6B2D8B),
                ),
              ),
              Text(
                'Welcome Teacher',
                style: TextStyle(
                  fontFamily: 'Merriweather',
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF3D3D3D),
                ),
              ),
            ],
          ),
          Container(
            width: 60,
            height: 60,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(color: const Color(0xFF6B2D8B), width: 2),
            ),
            child: ClipOval(
              child: Image.asset(
                'assets/images/teacher.png',
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) {
                  return const Icon(Icons.person, size: 35, color: Color(0xFF6B2D8B));
                },
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ---------- Mapa con forma de mancha ----------
  Widget _buildMapaBlob(Size size) {
    return Center(
      child: SizedBox(
        width: size.width * 0.88,
        height: size.height * 0.30,
        child: ClipPath(
          clipper: _BlobClipper(),
          child: Container(
            decoration: const BoxDecoration(
              color: Colors.white,
            ),
            child: Stack(
              children: [
                // Marcador de posición del mapa
                Container(
                  color: const Color(0xFFE8E0EF),
                  child: const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.map_outlined, size: 50, color: Color(0xFFA98BC3)),
                        SizedBox(height: 8),
                        Text(
                          'Tu ubicación',
                          style: TextStyle(
                            fontFamily: 'Merriweather',
                            fontSize: 15,
                            color: Color(0xFF6B2D8B),
                          ),
                        ),
                        SizedBox(height: 4),
                        Text(
                          'Mapa en tiempo real',
                          style: TextStyle(fontSize: 11, color: Color(0xFF9E9E9E)),
                        ),
                      ],
                    ),
                  ),
                ),
                // Botón mi ubicación
                const Positioned(
                  top: 15,
                  right: 15,
                  child: CircleAvatar(
                    backgroundColor: Color(0xFFA98BC3),
                    radius: 16,
                    child: Icon(Icons.my_location, color: Colors.white, size: 18),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // ---------- Fecha y Hora ----------
  Widget _buildFechaHora() {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 30),
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withValues(alpha: 0.1),
            blurRadius: 8,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.access_time, color: Color(0xFF6B2D8B), size: 24),
          const SizedBox(width: 12),
          Column(
            children: [
              Text(
                _horaActual,
                style: const TextStyle(
                  fontFamily: 'Merriweather',
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF6B2D8B),
                ),
              ),
              const SizedBox(height: 2),
              Text(
                _fechaActual,
                style: const TextStyle(
                  fontFamily: 'Merriweather',
                  fontSize: 12,
                  color: Color(0xFF757575),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  // ---------- Estado ----------
  Widget _buildEstado() {
    String texto;
    Color color;
    IconData icono;

    if (!_dentroDelPerimetro) {
      texto = 'Fuera del perímetro';
      color = const Color(0xFFC62828);
      icono = Icons.cancel;
    } else if (_salidaRegistrada) {
      texto = 'Jornada completada';
      color = const Color(0xFF2E7D32);
      icono = Icons.check_circle;
    } else if (_entradaRegistrada) {
      texto = 'Entrada registrada';
      color = const Color(0xFF1565C0);
      icono = Icons.check_circle_outline;
    } else {
      texto = 'Dentro del perímetro';
      color = const Color(0xFF2E7D32);
      icono = Icons.check_circle;
    }

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 30),
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withValues(alpha: 0.1),
            blurRadius: 8,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icono, color: color, size: 24),
          const SizedBox(width: 10),
          Text(
            texto,
            style: TextStyle(
              fontFamily: 'Merriweather',
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
        ],
      ),
    );
  }

  // ---------- Botones de registro ----------
  Widget _buildBotones(Size size) {
    // Entrada activa si: está dentro del perímetro Y no ha registrado entrada
    final bool entradaActiva = _dentroDelPerimetro && !_entradaRegistrada;
    // Salida activa si: está dentro del perímetro Y ya registró entrada Y no ha registrado salida
    final bool salidaActiva =
        _dentroDelPerimetro && _entradaRegistrada && !_salidaRegistrada;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 30),
      child: Row(
        children: [
          // Botón de ENTRADA
          Expanded(
            child: SizedBox(
              height: 55,
              child: DecoratedBox(
                decoration: BoxDecoration(
                  gradient: entradaActiva
                      ? const LinearGradient(
                          colors: [Color(0xFFA98BC3), Color(0xFFE8A0BF)],
                        )
                      : const LinearGradient(
                          colors: [Color(0xFFBDBDBD), Color(0xFFE0E0E0)],
                        ),
                  borderRadius: BorderRadius.circular(25),
                  boxShadow: entradaActiva
                      ? [
                          BoxShadow(
                            color: const Color(0xFFA98BC3).withValues(alpha: 0.4),
                            blurRadius: 10,
                            offset: const Offset(0, 5),
                          ),
                        ]
                      : [],
                ),
                child: ElevatedButton.icon(
                  onPressed: entradaActiva
                      ? () {
                          setState(() {
                            _entradaRegistrada = true;
                          });
                          _mostrarAlerta(
                            titulo: 'Entrada registrada',
                            mensaje: 'Tu entrada ha sido registrada correctamente a las $_horaActual',
                            color: const Color(0xFF2E7D32),
                            icono: Icons.login,
                          );
                        }
                      : null,
                  icon: Icon(
                    Icons.login,
                    color: entradaActiva ? Colors.white : Colors.grey[600],
                  ),
                  label: Text(
                    'Entrada',
                    style: TextStyle(
                      fontFamily: 'Merriweather',
                      fontSize: 15,
                      fontWeight: FontWeight.bold,
                      color: entradaActiva ? Colors.white : Colors.grey[600],
                    ),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.transparent,
                    shadowColor: Colors.transparent,
                    disabledBackgroundColor: Colors.transparent,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(25),
                    ),
                  ),
                ),
              ),
            ),
          ),
          const SizedBox(width: 15),
          // Botón de SALIDA
          Expanded(
            child: SizedBox(
              height: 55,
              child: DecoratedBox(
                decoration: BoxDecoration(
                  gradient: salidaActiva
                      ? const LinearGradient(
                          colors: [Color(0xFF6B2D8B), Color(0xFFA98BC3)],
                        )
                      : const LinearGradient(
                          colors: [Color(0xFFBDBDBD), Color(0xFFE0E0E0)],
                        ),
                  borderRadius: BorderRadius.circular(25),
                  boxShadow: salidaActiva
                      ? [
                          BoxShadow(
                            color: const Color(0xFF6B2D8B).withValues(alpha: 0.3),
                            blurRadius: 10,
                            offset: const Offset(0, 5),
                          ),
                        ]
                      : [],
                ),
                child: ElevatedButton.icon(
                  onPressed: salidaActiva
                      ? () {
                          setState(() {
                            _salidaRegistrada = true;
                          });
                          _mostrarAlerta(
                            titulo: 'Salida registrada',
                            mensaje: 'Tu salida ha sido registrada correctamente a las $_horaActual',
                            color: const Color(0xFF6B2D8B),
                            icono: Icons.logout,
                          );
                        }
                      : null,
                  icon: Icon(
                    Icons.logout,
                    color: salidaActiva ? Colors.white : Colors.grey[600],
                  ),
                  label: Text(
                    'Salida',
                    style: TextStyle(
                      fontFamily: 'Merriweather',
                      fontSize: 15,
                      fontWeight: FontWeight.bold,
                      color: salidaActiva ? Colors.white : Colors.grey[600],
                    ),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.transparent,
                    shadowColor: Colors.transparent,
                    disabledBackgroundColor: Colors.transparent,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(25),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ---------- Alerta personalizada ----------
  void _mostrarAlerta({
    required String titulo,
    required String mensaje,
    required Color color,
    required IconData icono,
  }) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            CircleAvatar(
              backgroundColor: color.withValues(alpha: 0.15),
              radius: 35,
              child: Icon(icono, color: color, size: 35),
            ),
            const SizedBox(height: 18),
            Text(
              titulo,
              style: TextStyle(
                fontFamily: 'Merriweather',
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            const SizedBox(height: 10),
            Text(
              mensaje,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontFamily: 'Merriweather',
                fontSize: 13,
                color: Color(0xFF757575),
              ),
            ),
          ],
        ),
        actions: [
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () => Navigator.pop(context),
              style: ElevatedButton.styleFrom(
                backgroundColor: color,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(15),
                ),
                padding: const EdgeInsets.symmetric(vertical: 12),
              ),
              child: const Text(
                'Aceptar',
                style: TextStyle(
                  fontFamily: 'Merriweather',
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ---------- Barra de navegación inferior ----------
  Widget _buildBottomNav() {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(25),
          topRight: Radius.circular(25),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withValues(alpha: 0.2),
            blurRadius: 15,
            offset: const Offset(0, -5),
          ),
        ],
      ),
      child: ClipRRect(
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(25),
          topRight: Radius.circular(25),
        ),
        child: BottomNavigationBar(
          currentIndex: 0,
          onTap: (index) {
            if (index == 4) {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(builder: (_) => const LoginScreen()),
              );
            }
          },
          type: BottomNavigationBarType.fixed,
          backgroundColor: Colors.white,
          selectedItemColor: const Color(0xFF6B2D8B),
          unselectedItemColor: Colors.grey,
          selectedLabelStyle: const TextStyle(
            fontFamily: 'Merriweather',
            fontSize: 11,
            fontWeight: FontWeight.bold,
          ),
          unselectedLabelStyle: const TextStyle(
            fontFamily: 'Merriweather',
            fontSize: 10,
          ),
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.location_on_outlined),
              activeIcon: Icon(Icons.location_on),
              label: 'Marcar',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.calendar_today_outlined),
              activeIcon: Icon(Icons.calendar_today),
              label: 'Horario',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.history_outlined),
              activeIcon: Icon(Icons.history),
              label: 'Registros',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.person_outline),
              activeIcon: Icon(Icons.person),
              label: 'Perfil',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.logout, color: Colors.red),
              label: 'Salir',
            ),
          ],
        ),
      ),
    );
  }
}

// ---------- Recortador personalizado para forma de mancha ----------
class _BlobClipper extends CustomClipper<Path> {
  @override
  Path getClip(Size size) {
    final path = Path();
    final w = size.width;
    final h = size.height;

    path.moveTo(w * 0.05, h * 0.15);
    path.cubicTo(w * 0.0, h * 0.0, w * 0.35, h * -0.05, w * 0.5, h * 0.03);
    path.cubicTo(w * 0.65, h * -0.02, w * 1.0, h * 0.0, w * 0.95, h * 0.18);
    path.cubicTo(w * 1.05, h * 0.35, w * 1.02, h * 0.65, w * 0.95, h * 0.80);
    path.cubicTo(w * 1.0, h * 1.0, w * 0.70, h * 1.05, w * 0.50, h * 0.98);
    path.cubicTo(w * 0.30, h * 1.05, w * 0.0, h * 1.0, w * 0.05, h * 0.82);
    path.cubicTo(w * -0.02, h * 0.65, w * -0.02, h * 0.35, w * 0.05, h * 0.15);
    path.close();

    return path;
  }

  @override
  bool shouldReclip(covariant CustomClipper<Path> oldClipper) => false;
}
