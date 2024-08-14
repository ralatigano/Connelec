from django.urls import path
from .views import (
    tareas, ver_tareas, crear_tarea,  info_editar_tarea, editar_tarea, borrar_tarea,
    ver_mis_tareas, tareas_asosc_proy, explorar_tarea,
    entradas_asosc_proy, crear_entrada, cargar_entradas, editar_entrada, borrar_entrada
)

urlpatterns = [
    # Menu tareas
    path('', tareas, name='tareas'),
    # CRUD Tareas
    path('verTareas', ver_tareas, name='verTareas'),
    path('crearTarea', crear_tarea, name='crearTarea'),
    path('infoEditarTarea', info_editar_tarea, name='infoEditarTarea'),
    path('editarTarea', editar_tarea, name='editarTarea'),
    path('borrarTarea/<int:id>', borrar_tarea, name='borrarTarea'),
    # Vistas adicionales de tareas, filtradas por proyecto, por encargado o vista de una tarea en detalle
    path('verMisTareas', ver_mis_tareas, name='verMisTareas'),
    path('porProyecto/<str:proy>', tareas_asosc_proy, name='tareasAsocProyecto'),
    path('explorarTarea/<str:nombTarea>', explorar_tarea, name='explorarTarea'),
    # CRUD Entradas historial de un proyecto
    path('historico/<str:proy>', entradas_asosc_proy,
         name='entradasAsocProyecto'),
    path('crearEntrada/<str:proy>', crear_entrada, name='crearEntrada'),
    path('cargarEntradas', cargar_entradas, name='cargarEntradas'),
    path('editarEntrada', editar_entrada, name='editarEntrada'),
    path('borrarEntrada/<int:id>', borrar_entrada, name='borrarEntrada'),
]
