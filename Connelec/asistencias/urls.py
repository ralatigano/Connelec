
from django.urls import path
from .views import (
    asistencia, hoy, ver_periodo,
    marcar_asistencia, listar_registros, editar_registro, borrar_registro, enviar_asistencia,
    reportes, crear_reporte, ver_reportes, editar_reporte, borrar_reporte
)

urlpatterns = [
    # Menu asistencias
    path('', asistencia, name='asistencias'),
    # Vistas para calcular horas trabajadas en determinados periodos de tiempo según las asistencias registradas
    path('hoy', hoy, name='hoy'),
    path('verPeriodo', ver_periodo, name='verPeriodo'),
    # CRUD Registros
    path('verAsistencias', listar_registros, name='verAsistencias'),
    path('enviar_asistencia', enviar_asistencia, name='enviarAsistencia'),
    path('marcarAsistencia', marcar_asistencia, name='marcarAsistencia'),
    path('editarRegistro', editar_registro, name='editarRegistro'),
    path('borrarRegistro/<int:id>', borrar_registro, name='borrarRegistro'),
    # Menu reportes
    path('reportes', reportes, name='reportes'),
    # CRUD Reportes
    path('verReportes', ver_reportes, name='verReportes'),
    path('crearReporte', crear_reporte, name='crearReporte'),
    path('editarReporte', editar_reporte, name='editarReporte'),
    path('borrarReporte/<int:id>', borrar_reporte, name='borrarReporte'),
]
