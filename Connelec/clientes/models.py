from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=100, blank=True)
    cuit = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    provincia = models.CharField(max_length=50, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):  
        return self.nombre
    
    def Meta(self):
        verbose_name = "cliente"
        verbose_name_plural = "clientes"