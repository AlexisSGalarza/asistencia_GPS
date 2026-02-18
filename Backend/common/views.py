from rest_framework.views import APIView
from django.http import FileResponse
from common.permissions import EsSupervisorOAdmin
from common.reportes import generar_reporte_asistencia, generar_reporte_incidencias
from apps.locations.models import Asistencia, Incidencia


class ReporteAsistenciaPDFView(APIView):
    """
    GET /api/reportes/asistencia/?fecha_inicio=2026-01-01&fecha_fin=2026-01-31&usuario=1
    Descarga un PDF con el reporte de asistencias.
    """
    permission_classes = [EsSupervisorOAdmin]

    def get(self, request):
        qs = Asistencia.objects.select_related('usuario', 'perimetro').all()

        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        usuario_id = request.query_params.get('usuario')

        if usuario_id:
            qs = qs.filter(usuario_id=usuario_id)
        if fecha_inicio:
            qs = qs.filter(fecha_hora__date__gte=fecha_inicio)
        if fecha_fin:
            qs = qs.filter(fecha_hora__date__lte=fecha_fin)

        qs = qs.order_by('fecha_hora')

        buffer = generar_reporte_asistencia(
            list(qs),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )

        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f'reporte_asistencia_{fecha_inicio or "completo"}.pdf',
            content_type='application/pdf',
        )


class ReporteIncidenciasPDFView(APIView):
    """
    GET /api/reportes/incidencias/?fecha_inicio=2026-01-01&fecha_fin=2026-01-31&usuario=1
    Descarga un PDF con el reporte de incidencias.
    """
    permission_classes = [EsSupervisorOAdmin]

    def get(self, request):
        qs = Incidencia.objects.select_related('usuario').all()

        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        usuario_id = request.query_params.get('usuario')

        if usuario_id:
            qs = qs.filter(usuario_id=usuario_id)
        if fecha_inicio:
            qs = qs.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            qs = qs.filter(fecha__lte=fecha_fin)

        qs = qs.order_by('fecha')

        buffer = generar_reporte_incidencias(
            list(qs),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )

        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f'reporte_incidencias_{fecha_inicio or "completo"}.pdf',
            content_type='application/pdf',
        )
