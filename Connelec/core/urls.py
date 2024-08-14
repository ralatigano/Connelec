from django.contrib import admin
from django.urls import path
from .views import (
    registrarse, inicio, cerrar_sesion, iniciar_sesion,
    editar_perfil, cambiar_contrasena, restablecer_contrasena, correo_contrasena,
    dark_mode, get_dark_mode)
from django.contrib.auth.views import LoginView

urlpatterns = [
    # path('registrarse', registrarse, name='registrarse'),
    # Login y Logout
    path('', iniciar_sesion, name='login'),
    path('logout', cerrar_sesion, name='logout'),
    # Home
    path('inicio', inicio, name='inicio'),
    # Edición de perfil
    path('perfil', editar_perfil, name='perfil'),
    path('cambiarContrasena', cambiar_contrasena, name='cambiarContrasena'),
    # Restablecer contraseña
    path('restablecerContrasena', restablecer_contrasena,
         name='restablecerContrasena'),
    path('correoContrasena', correo_contrasena, name='correoContrasena'),
    # Preferencia de tema oscuro/claro
    path('valorDarkMode/<str:tema>', dark_mode, name='valorDarkMode'),
    path('getDarkMode', get_dark_mode, name='getDarkMode'),
]
