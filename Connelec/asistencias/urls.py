
from django.urls import path, re_path
from .views import (
    asistencia, hoy, ver_periodo,
    marcar_asistencia, listar_registros, editar_registro, borrar_registro, enviar_asistencia, exportar_registros,
    ver_ausencias, obtener_ausencia, guardar_ausencia, borrar_ausencia, eliminar_archivo,
    reportes, crear_reporte, ver_reportes, editar_reporte, borrar_reporte, exportar_reportes,
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
    path('exportarRegistros', exportar_registros, name='exportarRegistros'),
    # CRUD Ausencias
    path('verAusencias', ver_ausencias, name='verAusencias'),
    re_path(r'^obtenerAusencia/(?P<ausencia_id>(new|\d+))/$',
            obtener_ausencia, name='obtenerAusencia'),
    path('guardarAusencia', guardar_ausencia, name='guardarAusencia'),
    path('borrarAusencia/<int:id>', borrar_ausencia, name='borrarAusencia'),
    path('eliminarArchivo/<int:aucencia_id>',
         eliminar_archivo, name='eliminarArchivo'),
    # Menu reportes
    path('reportes', reportes, name='reportes'),
    # CRUD Reportes
    path('verReportes', ver_reportes, name='verReportes'),
    path('crearReporte', crear_reporte, name='crearReporte'),
    path('editarReporte', editar_reporte, name='editarReporte'),
    path('borrarReporte/<int:id>', borrar_reporte, name='borrarReporte'),
    path('exportarReportes', exportar_reportes, name='exportarReportes'),
]
