from django.urls import path
from .views import (
    tareas, crear_tarea, ver_tareas, ver_mis_tareas, info_editar_tarea,
    editar_tarea, tareas_asosc_proy, explorar_tarea, entradas_asosc_proy,
    crear_entrada, editar_entrada, borrar_entrada
)

urlpatterns = [
    path('', tareas, name='tareas'),
    path('crearTarea', crear_tarea, name='crearTarea'),
    path('verTareas', ver_tareas, name='verTareas'),
    path('verMisTareas', ver_mis_tareas, name='verMisTareas'),
    path('infoEditarTarea', info_editar_tarea, name='infoEditarTarea'),
    path('editarTarea', editar_tarea, name='editarTarea'),
    path('porProyecto/<str:proy>', tareas_asosc_proy, name='tareasAsocProyecto'),
    path('explorarTarea/<str:nombTarea>', explorar_tarea, name='explorarTarea'),
    path('historico/<str:proy>', entradas_asosc_proy,
         name='entradasAsocProyecto'),
    path('crearEntrada/<str:proy>', crear_entrada, name='crearEntrada'),
    path('editarEntrada', editar_entrada, name='editarEntrada'),
    path('borrarEntrada/<int:id>', borrar_entrada, name='borrarEntrada'),
]
