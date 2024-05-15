
from django.urls import path
from .views import (
                    asistencia, marcar_asistencia, hoy, listar_registros,
                    ver_periodo, reportes, ver_reportes, crear_reporte,
                    editar_reporte
)

urlpatterns = [
    path('', asistencia, name='asistencias'),
    path('marcarAsistencia', marcar_asistencia, name='marcarAsistencia'),
    path('hoy', hoy, name='hoy'),
    path('verAsistencias', listar_registros, name='verAsistencias'),
    path('verPeriodo', ver_periodo, name='verPeriodo'),
    path('reportes', reportes, name='reportes'),
    path('verReportes', ver_reportes, name='verReportes'),
    path('crearReporte', crear_reporte, name='crearReporte'),
    path('editarReporte', editar_reporte, name='editarReporte'),
]