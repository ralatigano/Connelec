from django.urls import path
from .views import (proyectos,
                    ver_proyectos, crear_proyecto, info_editar_proyecto, editar_proyecto, borrar_proyecto
                    )


urlpatterns = [
    # Menu proyectos
    path('', proyectos, name='proyectos'),
    # CRUD Proyectos
    path('verProyectos', ver_proyectos, name='verProyectos'),
    path('crearProyecto', crear_proyecto, name='crearProyecto'),
    path('infoEditarProyecto', info_editar_proyecto, name='infoEditarProyecto'),
    path('editarProyecto', editar_proyecto, name='editarProyecto'),
    path('borrarProyecto/<int:id>', borrar_proyecto, name='borrarProyecto')
]
