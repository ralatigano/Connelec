from django.db import models

# Create your models here.
class Proyectos(models.Model):
    nombre = models.CharField(max_length=100)
    cliente = models.ForeignKey("clientes.Cliente", on_delete=models.CASCADE, default=None, blank=True)
    descripcion = models.TextField(max_length=500, blank=True)
    n_expediente = models.CharField(max_length=100, blank=True, default=None, null=True)
    #tareas = models.ManyToManyField("tareas.Tareas", blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def Meta(self):
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos"