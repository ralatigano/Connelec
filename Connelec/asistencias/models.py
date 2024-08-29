from django.db import models
import os
from django.conf import settings
from PIL import Image
from django.contrib.auth.models import User
from proyectos.models import Proyectos
from django.core.files.storage import default_storage
from .functions import *


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=profile_picture_path, blank=True)
    birthday = models.DateField(null=True, blank=True)
    dark_mode = models.BooleanField(default=False)
    telefono = models.CharField(
        max_length=20, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if self.pk and self.image:
            old_profile = Usuario.objects.get(pk=self.pk) if self.pk else None
            if old_profile.image and old_profile.image.path != self.image.path:
                default_storage.delete(old_profile.image.path)
        super(Usuario, self).save(*args, **kwargs)
        if self.image and os.path.exists(self.image.path):
            self.resize_image()

    def resize_image(self):
        with Image.open(self.image.path) as img:
            ancho, alto = img.size
            if ancho > alto:
                nuevo_alto = 300
                nuevo_ancho = int((ancho/alto)*nuevo_alto)
                img = img.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
                img.save(self.image.path)
            elif alto > ancho:
                nuevo_ancho = 300
                nuevo_alto = int((alto/ancho)*nuevo_ancho)
                img = img.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
                img.save(self.image.path)
            else:
                img.thumbnail((300, 300), Image.LANCZOS)
                img.save(self.image.path)
        with Image.open(self.image.path) as img:
            ancho, alto = img.size
            if ancho > alto:
                left = (ancho - alto) / 2
                top = 0
                right = (ancho + alto) / 2
                bottom = alto
            else:
                left = 0
                top = (alto - ancho) / 2
                right = ancho
                bottom = (alto + ancho) / 2
            img = img.crop((left, top, right, bottom))
            img.save(self.image.path)


class Reporte_tarea(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    proyecto = models.ForeignKey(
        Proyectos, on_delete=models.CASCADE, default=None, blank=True, null=True)
    informe = models.CharField(max_length=1000)


class AusenciaJustificada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.CharField(max_length=255)
    cantidad_dias = models.PositiveIntegerField()
    archivo = models.FileField(
        upload_to=user_ausencia_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_record = AusenciaJustificada.objects.get(pk=self.pk)
                # Si hay un archivo antiguo y es diferente del archivo nuevo
                if old_record.archivo and (self.archivo and old_record.archivo != self.archivo):
                    old_record.archivo.delete(save=False)
                # Si el archivo se ha eliminado y no se está agregando uno nuevo
                elif not self.archivo and old_record.archivo:
                    old_record.archivo.delete(save=False)
            except AusenciaJustificada.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ausencia de {self.usuario.username} del {self.fecha_inicio} al {self.fecha_fin}"


class registro(models.Model):
    # cambio esto para probar un modelo de usuario con una relación OneToOneField con User
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE)  # usuario = models.ForeignKey(
    # settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    tipo = models.CharField(max_length=50, choices=[(
        'Entrada', 'Entrada'), ('Salida', 'Salida')])

    def __str__(self):
        return (f"{self.usuario} - {self.tipo} - {self.fecha.strftime('%d/%m/%Y')}")

    @property
    def nombre_completo(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"
