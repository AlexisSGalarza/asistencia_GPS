from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PerimetroViewSet, AsistenciaViewSet

router = DefaultRouter()
router.register(r'perimetros', PerimetroViewSet, basename='perimetro')
router.register(r'asistencias', AsistenciaViewSet, basename='asistencia')

urlpatterns = [
    path('', include(router.urls)),
]
