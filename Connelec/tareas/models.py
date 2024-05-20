from django.db import models
from django.conf import settings
from proyectos.models import Proyectos

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
    encargado = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True, null=True)
    estado = models.CharField(
        max_length=30, choices=opciones_estado, default='Sin asignar')
    fecha_entrega = models.DateField(default=None, blank=True, null=True)
    proyecto = models.ForeignKey(
        "proyectos.Proyectos", on_delete=models.CASCADE, default=None, blank=True, null=True)
    # archivos = models.ManyToManyField("Archivos", blank=True)
    # historial = models.ForeignKey("Historial", on_delete=models.CASCADE, default=None, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def Meta(self):
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"


class Entrada_historial(models.Model):
    fecha = models.DateTimeField(null=True, blank=True, default=None)
    # usuario = models.ForeignKey(
    #    settings.AUTH_USER_MODEL, on_delete = models.CASCADE, default = None, blank = True, null = True)
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
