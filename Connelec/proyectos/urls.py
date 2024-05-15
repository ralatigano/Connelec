from django.urls import path
from .views import proyectos, ver_proyectos, crear_proyecto, editar_proyecto


urlpatterns = [
    path('', proyectos, name='proyectos'),
    path('verProyectos', ver_proyectos, name='verProyectos'),
    path('crearProyecto', crear_proyecto, name='crearProyecto'),
    path('editarProyecto', editar_proyecto, name='editarProyecto'),
]