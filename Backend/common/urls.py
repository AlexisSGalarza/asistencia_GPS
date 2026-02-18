from django.urls import path
from . import views

urlpatterns = [
    path('asistencia/', views.ReporteAsistenciaPDFView.as_view(), name='reporte-asistencia'),
    path('incidencias/', views.ReporteIncidenciasPDFView.as_view(), name='reporte-incidencias'),
]
