from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Perimetro, Asistencia
from .serializers import PerimetroSerializer, AsistenciaSerializer
from apps.users.models import Usuario

class PerimetroViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar perímetros GPS de las escuelas
    """
    queryset = Perimetro.objects.all()
    serializer_class = PerimetroSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """
        Obtener solo los perímetros activos
        """
        perimetros = self.queryset.filter(activo=True)
        serializer = self.get_serializer(perimetros, many=True)
        return Response(serializer.data)

class AsistenciaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar el registro de asistencias
    """
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def registrar(self, request):
        """
        Registrar una entrada o salida
        Valida automáticamente si está dentro del perímetro
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            asistencia = serializer.save()
            
            if asistencia.valido:
                mensaje = f'Asistencia ({asistencia.tipo}) registrada correctamente'
                status_code = status.HTTP_201_CREATED
            else:
                mensaje = f'Asistencia registrada pero FUERA del perímetro permitido'
                status_code = status.HTTP_201_CREATED
            
            return Response({
                'mensaje': mensaje,
                'asistencia': AsistenciaSerializer(asistencia).data
            }, status=status_code)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def historial(self, request):
        """
        Obtener historial de asistencias de un usuario
        """
        usuario_id = request.query_params.get('usuario_id')
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        
        if not usuario_id:
            return Response(
                {'error': 'usuario_id es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        asistencias = self.queryset.filter(usuario_id=usuario_id)
        
        # Filtrar por rango de fechas si se proporciona
        if fecha_inicio:
            asistencias = asistencias.filter(fecha_hora__gte=fecha_inicio)
        if fecha_fin:
            asistencias = asistencias.filter(fecha_hora__lte=fecha_fin)
        
        asistencias = asistencias.order_by('-fecha_hora')
        serializer = self.get_serializer(asistencias, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def hoy(self, request):
        """
        Obtener asistencias del día actual
        """
        hoy = timezone.now().date()
        asistencias = self.queryset.filter(fecha_hora__date=hoy)
        
        # Si se proporciona usuario_id, filtrar por ese usuario
        usuario_id = request.query_params.get('usuario_id')
        if usuario_id:
            asistencias = asistencias.filter(usuario_id=usuario_id)
        
        serializer = self.get_serializer(asistencias, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def reporte(self, request):
        """
        Generar datos para reporte de asistencias
        """
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        
        asistencias = self.queryset.all()
        
        if fecha_inicio:
            asistencias = asistencias.filter(fecha_hora__gte=fecha_inicio)
        if fecha_fin:
            asistencias = asistencias.filter(fecha_hora__lte=fecha_fin)
        
        # Agrupar datos para el reporte
        datos_reporte = []
        usuarios = Usuario.objects.all()
        
        for usuario in usuarios:
            asist_usuario = asistencias.filter(usuario=usuario)
            total = asist_usuario.count()
            validas = asist_usuario.filter(valido=True).count()
            invalidas = total - validas
            
            datos_reporte.append({
                'usuario': usuario.nombre,
                'correo': usuario.correo,
                'total_registros': total,
                'registros_validos': validas,
                'registros_invalidos': invalidas
            })
        
        return Response({
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'datos': datos_reporte
        })

