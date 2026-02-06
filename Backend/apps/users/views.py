from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import check_password
from .models import Rol, Usuario, Horario
from .serializers import RolSerializer, UsuarioSerializer, HorarioSerializer

class RolViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar roles (Administrador, Supervisor, Maestro)
    """
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        # Permitir acceso sin autenticación para el login
        if self.action == 'login':
            return [AllowAny()]
        return super().get_permissions()
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Endpoint de login básico
        """
        correo = request.data.get('correo')
        password = request.data.get('password')
        
        if not correo or not password:
            return Response(
                {'error': 'Correo y contraseña son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            usuario = Usuario.objects.get(correo=correo, activo=True)
            # En producción deberías usar hash para comparar contraseñas
            if usuario.password == password:
                serializer = self.get_serializer(usuario)
                return Response({
                    'mensaje': 'Login exitoso',
                    'usuario': serializer.data
                })
            else:
                return Response(
                    {'error': 'Credenciales inválidas'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Obtener información del usuario actual (basado en el token)
        """
        # Esta funcionalidad se implementará completamente con JWT
        return Response({'mensaje': 'Endpoint para obtener usuario actual'})
    
    @action(detail=False, methods=['get'])
    def maestros(self, request):
        """
        Listar solo usuarios con rol de maestro
        """
        maestros = self.queryset.filter(rol__nombre='Maestro')
        serializer = self.get_serializer(maestros, many=True)
        return Response(serializer.data)

class HorarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar horarios de los usuarios
    """
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def mis_horarios(self, request):
        """
        Obtener horarios del usuario actual
        """
        # Cuando implementes JWT, obtendrías el usuario del token
        usuario_id = request.query_params.get('usuario_id')
        if usuario_id:
            horarios = self.queryset.filter(usuario_id=usuario_id)
            serializer = self.get_serializer(horarios, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'usuario_id es requerido'},
            status=status.HTTP_400_BAD_REQUEST
        )

