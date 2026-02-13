from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.utils import timezone
from datetime import date, timedelta, datetime

from common.permissions import EsAdministrador, EsSupervisorOAdmin, EsUsuarioAutenticado
from apps.users.models import Usuario, Rol

from .models import Perimetro, Asistencia, Incidencia
from .serializers import (
    PerimetroSerializer, AsistenciaSerializer,
    RegistrarAsistenciaSerializer, IncidenciaSerializer,
)


# ──────────────────────────────────────────────
# REGISTRO DE ASISTENCIA POR GPS
# ──────────────────────────────────────────────

class RegistrarAsistenciaView(APIView):
    """
    POST /api/asistencia/registrar/
    El maestro envía su lat/lng y tipo (entrada/salida).
    El sistema valida si está dentro del perímetro.
    """
    permission_classes = [EsUsuarioAutenticado]

    def post(self, request):
        serializer = RegistrarAsistenciaSerializer(
            data=request.data,
            context={'usuario': request.usuario},
        )
        serializer.is_valid(raise_exception=True)
        asistencia = serializer.save()

        response_data = AsistenciaSerializer(asistencia).data
        if asistencia.valido:
            response_data['mensaje'] = 'Asistencia registrada correctamente.'
        else:
            response_data['mensaje'] = (
                f'Estás fuera del perímetro. '
                f'Distancia: {asistencia.distancia_metros}m '
                f'(máximo permitido: {asistencia.perimetro.radio_metros}m). '
                f'Se registró como INVÁLIDA.'
            )

        return Response(response_data, status=status.HTTP_201_CREATED)


# ──────────────────────────────────────────────
# HISTORIAL DE ASISTENCIA (Req. 3)
# ──────────────────────────────────────────────

class HistorialAsistenciaView(APIView):
    """
    GET /api/asistencia/historial/
    Cada maestro consulta su propio historial.
    Query params opcionales: ?fecha_inicio=2026-01-01&fecha_fin=2026-01-31
    """
    permission_classes = [EsUsuarioAutenticado]

    def get(self, request):
        asistencias = Asistencia.objects.filter(
            usuario=request.usuario,
        ).select_related('perimetro')

        # Filtros opcionales por fecha
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        if fecha_inicio:
            asistencias = asistencias.filter(fecha_hora__date__gte=fecha_inicio)
        if fecha_fin:
            asistencias = asistencias.filter(fecha_hora__date__lte=fecha_fin)

        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response(serializer.data)


# ──────────────────────────────────────────────
# PANEL DE SUPERVISIÓN (Req. 4)
# ──────────────────────────────────────────────

class PanelSupervisionView(APIView):
    """
    GET /api/asistencia/panel/
    Supervisores y admins ven el estado de asistencia de hoy.
    Query params opcionales: ?fecha=2026-02-06
    """
    permission_classes = [EsSupervisorOAdmin]

    def get(self, request):
        fecha = request.query_params.get('fecha', str(date.today()))

        # Todos los maestros activos
        maestros = Usuario.objects.filter(
            rol__nombre=Rol.Nombre.MAESTRO,
            activo=True,
        ).select_related('rol')

        resultado = []
        for maestro in maestros:
            asistencias_hoy = Asistencia.objects.filter(
                usuario=maestro,
                fecha_hora__date=fecha,
            ).order_by('fecha_hora')

            entrada = asistencias_hoy.filter(tipo=Asistencia.Tipo.ENTRADA).first()
            salida = asistencias_hoy.filter(tipo=Asistencia.Tipo.SALIDA).last()

            incidencias_hoy = Incidencia.objects.filter(
                usuario=maestro,
                fecha=fecha,
            )

            resultado.append({
                'maestro': {
                    'id': maestro.id,
                    'nombre': maestro.nombre,
                    'correo': maestro.correo,
                },
                'entrada': AsistenciaSerializer(entrada).data if entrada else None,
                'salida': AsistenciaSerializer(salida).data if salida else None,
                'incidencias': IncidenciaSerializer(incidencias_hoy, many=True).data,
                'estado': self._calcular_estado(entrada, salida),
            })

        return Response({
            'fecha': fecha,
            'total_maestros': len(resultado),
            'maestros': resultado,
        })

    def _calcular_estado(self, entrada, salida):
        """Calcula el estado del maestro basado en sus registros."""
        if not entrada:
            return 'sin_registro'
        if entrada and not entrada.valido:
            return 'fuera_de_perimetro'
        if entrada and not salida:
            return 'en_turno'
        if entrada and salida:
            return 'turno_completado'
        return 'desconocido'


# ──────────────────────────────────────────────
# ADMIN: ASISTENCIA COMPLETA
# ──────────────────────────────────────────────

class AsistenciaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/asistencia/         → Lista todas (admin/supervisor)
    GET /api/asistencia/{id}/    → Detalle
    Query params: ?usuario=1&fecha_inicio=2026-01-01&fecha_fin=2026-01-31
    """
    serializer_class = AsistenciaSerializer
    permission_classes = [EsSupervisorOAdmin]

    def get_queryset(self):
        qs = Asistencia.objects.select_related('usuario', 'perimetro').all()

        # Filtros opcionales
        usuario_id = self.request.query_params.get('usuario')
        fecha_inicio = self.request.query_params.get('fecha_inicio')
        fecha_fin = self.request.query_params.get('fecha_fin')
        solo_validos = self.request.query_params.get('valido')

        if usuario_id:
            qs = qs.filter(usuario_id=usuario_id)
        if fecha_inicio:
            qs = qs.filter(fecha_hora__date__gte=fecha_inicio)
        if fecha_fin:
            qs = qs.filter(fecha_hora__date__lte=fecha_fin)
        if solo_validos is not None:
            qs = qs.filter(valido=solo_validos.lower() == 'true')

        return qs


# ──────────────────────────────────────────────
# ADMIN: PERÍMETROS (Req. 6)
# ──────────────────────────────────────────────

class PerimetroViewSet(viewsets.ModelViewSet):
    """
    CRUD de perímetros. Solo administradores.
    """
    queryset = Perimetro.objects.all()
    serializer_class = PerimetroSerializer
    permission_classes = [EsAdministrador]


# ──────────────────────────────────────────────
# ADMIN: INCIDENCIAS
# ──────────────────────────────────────────────

class IncidenciaViewSet(viewsets.ModelViewSet):
    """
    CRUD de incidencias.
    Maestros ven las suyas, admin/supervisor ven todas.
    """
    serializer_class = IncidenciaSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [EsUsuarioAutenticado()]
        return [EsSupervisorOAdmin()]

    def get_queryset(self):
        usuario = self.request.usuario
        qs = Incidencia.objects.select_related('usuario').all()

        if usuario.es_maestro:
            qs = qs.filter(usuario=usuario)

        # Filtros opcionales
        usuario_id = self.request.query_params.get('usuario')
        fecha = self.request.query_params.get('fecha')

        if usuario_id and not usuario.es_maestro:
            qs = qs.filter(usuario_id=usuario_id)
        if fecha:
            qs = qs.filter(fecha=fecha)

        return qs

