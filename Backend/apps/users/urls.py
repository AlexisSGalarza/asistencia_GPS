from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RolViewSet, UsuarioViewSet, HorarioViewSet

router = DefaultRouter()
router.register(r'roles', RolViewSet, basename='rol')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'horarios', HorarioViewSet, basename='horario')

urlpatterns = [
    path('', include(router.urls)),
]
