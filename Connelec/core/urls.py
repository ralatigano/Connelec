from django.contrib import admin
from django.urls import path
from .views import registrarse, inicio, cerrar_sesion, iniciar_sesion, editar_perfil, cambiar_contrasena
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('registrarse', registrarse, name='registrarse'),
    path('', iniciar_sesion, name='login'),
    path('logout', cerrar_sesion, name='logout'),
    path('inicio', inicio, name='inicio'),
    path('perfil', editar_perfil, name='perfil'),
    path('cambiarContrasena', cambiar_contrasena, name='cambiarContrasena')
]
