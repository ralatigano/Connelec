from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from proyectos.models import Proyectos
import uuid
import os
from django.core.files.storage import default_storage
from PIL import Image

# User= get_user_model()

# Create your models here.


class registro(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # nombre = models.CharField(default=usuario.first_name, max_length=50, readonly=True, null=True)
    # apellido = models.CharField(default=usuario.last_name, max_length=50, readonly=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    tipo = models.CharField(max_length=50, choices=[(
        'Entrada', 'Entrada'), ('Salida', 'Salida')])

    def __str__(self):
        return (f"{self.usuario} - {self.tipo} - {self.fecha.strftime('%d/%m/%Y')}")

    @property
    def nombre_completo(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"

# Generar un nombre aleatorio usando la librería uuid


def profile_picture_path(instance, filename):
    random_filename = str(uuid.uuid4())
    # recupero la extensión del archivo de imagen
    extension = os.path.splitext(filename)[1]
    return 'users/{0}/{1}{2}'.format(instance.username, random_filename, extension)


class User(AbstractUser):
    image = models.ImageField(upload_to=profile_picture_path, blank=True)
    birthday = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        old_profile = User.objects.get(pk=self.pk) if self.pk else None
        default_storage.delete(old_profile.image.path)
        super(User, self).save(*args, **kwargs)

        if self.image and os.path.exists(self.image.path):
            # redimensionar la imagen antes de guardarla.
            with Image.open(self.image.path) as img:
                ancho, alto = img.size
                if ancho > alto:
                    nuevo_alto = 300
                    nuevo_ancho = int((ancho/alto)*nuevo_alto)
                    img = img.resize((nuevo_ancho, nuevo_alto))
                    img.save(self.image.path)
                if alto > ancho:
                    nuevo_ancho = 300
                    nuevo_alto = int((alto/ancho)*nuevo_ancho)
                    img = img.resize((nuevo_ancho, nuevo_alto))
                    img.save(self.image.path)
                else:
                    img.thumbnail((300, 300))
                    img.save(self.image.path)
            #   recorte final de la imagen
            with Image.open(self.image.path) as img:
                ancho, alto = img.size
                if ancho > alto:
                    left = (ancho-alto)/2
                    top = 0
                    right = (ancho + alto)/2
                    bottom = alto
                else:
                    left = 0
                    top = (alto-ancho)/2
                    right = ancho
                    bottom = (alto+ancho)/2
                img = img.crop((left, top, right, bottom))
                img.save(self.image.path)


class Reporte(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    proyecto = models.ForeignKey(
        Proyectos, on_delete=models.CASCADE, default=None, blank=True, null=True)
    informe = models.CharField(max_length=1000)
