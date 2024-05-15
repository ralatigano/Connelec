from django.db import models
from django.conf import settings

# Create your models here.

# opciones_estado = [
#     (0, 'Sin asignar'),
#     (1, 'Asignado/Sin iniciar'),
#     (2, 'En proceso'),
#     (3,'Hecho'),
# ]
# class Tareas(models.Model):
#     nombre = models.CharField(max_length=100)
#     descrip = models.TextField(max_length=500)
#     encargado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     estado = models.IntegerField(choices=opciones_estado, default=0)
#     fecha_entrega = models.DateField(default=None)
#     #archivos = models.ManyToManyField("Archivos", blank=True)
#     #historial = models.ForeignKey("Historial", on_delete=models.CASCADE, default=None, null=True, blank=True)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_actualizacion = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.nombre
    
#     def Meta(self):
#         verbose_name = "Tarea"
#         verbose_name_plural = "Tareas"

# class Entrada_historial(models.Model):
#     fecha_actualizacion = models.DateTimeField(auto_now=True)
#     resumen = models.TextField(max_length=1000)
#     tarea = models.ForeignKey("Tareas", on_delete=models.CASCADE)
#     adjunto = models.FileField(upload_to='archivos', blank=True)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.fecha_actualizacion
#     def Meta(self):
#         verbose_name = "entrada"
#         verbose_name_plural = "entradas"

# class Archivos(models.Model):
#     nombre = models.CharField(max_length=100)
#     tarea = models.ForeignKey(to="Tareas", on_delete=models.CASCADE)
#     archivo = models.FileField(upload_to='<tarea.nombre>/archivos', blank=True)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_actualización = models.DateTimeField(auto_now=True)

