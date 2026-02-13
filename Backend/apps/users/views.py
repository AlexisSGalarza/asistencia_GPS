from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from common.permissions import EsAdministrador, EsSupervisorOAdmin, EsUsuarioAutenticado
from common.authentication import generar_tokens

from .models import Rol, Usuario, Horario
from .serializers import (
    RolSerializer, UsuarioSerializer, UsuarioCreateSerializer,
    LoginSerializer, HorarioSerializer, CambiarPasswordSerializer,
)


# ──────────────────────────────────────────────
# AUTH ENDPOINTS
# ──────────────────────────────────────────────

class LoginView(APIView):
    """
    POST /api/auth/login/
    Recibe correo y password, devuelve tokens JWT + datos del usuario.
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # No requiere autenticación

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario = serializer.validated_data['usuario']
        tokens = generar_tokens(usuario)

        return Response({
            'tokens': tokens,
            'usuario': UsuarioSerializer(usuario).data,
        }, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    """
    POST /api/auth/refresh/
    Recibe un refresh token y devuelve un nuevo access token.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken
        from rest_framework_simplejwt.exceptions import TokenError

        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Se requiere el refresh token.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token),
            })
        except TokenError:
            return Response(
                {'error': 'Refresh token inválido o expirado.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class PerfilView(APIView):
    """
    GET  /api/auth/perfil/   → Datos del usuario autenticado
    PUT  /api/auth/perfil/   → Actualizar nombre/correo
    """
    permission_classes = [EsUsuarioAutenticado]

    def get(self, request):
        return Response(UsuarioSerializer(request.usuario).data)

    def put(self, request):
        usuario = request.usuario
        usuario.nombre = request.data.get('nombre', usuario.nombre)
        usuario.correo = request.data.get('correo', usuario.correo)
        usuario.save()
        return Response(UsuarioSerializer(usuario).data)


class CambiarPasswordView(APIView):
    """
    POST /api/auth/cambiar-password/
    Cambia la contraseña del usuario autenticado.
    """
    permission_classes = [EsUsuarioAutenticado]

    def post(self, request):
        serializer = CambiarPasswordSerializer(
            data=request.data,
            context={'usuario': request.usuario},
        )
        serializer.is_valid(raise_exception=True)

        request.usuario.set_password(serializer.validated_data['password_nuevo'])
        request.usuario.save()

        return Response({'mensaje': 'Contraseña actualizada correctamente.'})


# ──────────────────────────────────────────────
# ADMIN: CRUD DE USUARIOS (solo admin)
# ──────────────────────────────────────────────

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de usuarios. Solo accesible por administradores.
    GET    /api/usuarios/          → Lista todos
    POST   /api/usuarios/          → Crear usuario
    GET    /api/usuarios/{id}/     → Detalle
    PUT    /api/usuarios/{id}/     → Actualizar
    DELETE /api/usuarios/{id}/     → Desactivar (soft delete)
    """
    queryset = Usuario.objects.select_related('rol').all()
    permission_classes = [EsAdministrador]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UsuarioCreateSerializer
        return UsuarioSerializer

    def destroy(self, request, *args, **kwargs):
        """Soft delete: desactiva en vez de borrar."""
        usuario = self.get_object()
        usuario.activo = False
        usuario.save()
        return Response(
            {'mensaje': f'Usuario {usuario.nombre} desactivado.'},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=['get'], permission_classes=[EsSupervisorOAdmin])
    def maestros(self, request):
        """GET /api/usuarios/maestros/ → Lista solo maestros (para supervisores)."""
        maestros = Usuario.objects.filter(
            rol__nombre=Rol.Nombre.MAESTRO,
            activo=True,
        ).select_related('rol')
        serializer = UsuarioSerializer(maestros, many=True)
        return Response(serializer.data)


# ──────────────────────────────────────────────
# ADMIN: ROLES
# ──────────────────────────────────────────────

class RolViewSet(viewsets.ModelViewSet):
    """
    CRUD de roles. Solo administradores.
    """
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [EsAdministrador]


# ──────────────────────────────────────────────
# ADMIN: HORARIOS
# ──────────────────────────────────────────────

class HorarioViewSet(viewsets.ModelViewSet):
    """
    CRUD de horarios. Admin puede gestionar, maestros pueden ver los suyos.
    """
    serializer_class = HorarioSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [EsUsuarioAutenticado()]
        return [EsAdministrador()]

    def get_queryset(self):
        usuario = self.request.usuario
        if usuario.es_admin or usuario.es_supervisor:
            return Horario.objects.select_related('usuario').all()
        # Maestros solo ven sus propios horarios
        return Horario.objects.filter(usuario=usuario)

