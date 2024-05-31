from django.db import models
from django.conf import settings
from proyectos.models import Proyectos
from django.contrib.auth.models import User

# Create your models here.
opciones_estado = [
    ('Sin asignar', 'Sin asignar'),
    ('Asignado/Sin iniciar', 'Asignado/Sin iniciar'),
    ('En proceso', 'En proceso'),
    ('Hecho', 'Hecho'),
    ('En pausa', 'En pausa'),
    ('Cancelado', 'Cancelado'),
]


class Tareas(models.Model):
    nombre = models.CharField(max_length=100)
    descrip = models.TextField(max_length=500)
    # cambio esto para probar un modelo de usuario con una aplicación OneToOneField con User
    encargado = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    # encargado = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True, null=True)
    estado = models.CharField(
        max_length=30, choices=opciones_estado, default='Sin asignar')
    fecha_entrega = models.DateField(default=None, blank=True, null=True)
    proyecto = models.ForeignKey(
        "proyectos.Proyectos", on_delete=models.CASCADE, default=None, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_models')

    def __str__(self):
        return self.nombre

    def Meta(self):
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"


class Entrada_historial(models.Model):
    fecha = models.DateTimeField(null=True, blank=True, default=None)
    # cambio esto para probar un modelo de usuario con una aplicación OneToOneField con User
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    # usuario = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True, null=True)
    resumen = models.TextField(max_length=1000)
    proyecto = models.ForeignKey(
        "proyectos.Proyectos", on_delete=models.CASCADE)
    adjunto = models.FileField(upload_to='archivos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.fecha} - {self.resumen}'

    def Meta(self):
        verbose_name = "entrada"
        verbose_name_plural = "entradas"


class Archivos(models.Model):
    nombre = models.CharField(max_length=100)
    tarea = models.ForeignKey(to="Tareas", on_delete=models.CASCADE)
    archivo = models.FileField(
        upload_to='archivos/', blank=True, default=None, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualización = models.DateTimeField(auto_now=True)
