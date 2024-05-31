from django.db import models
# from django.contrib.auth.models import User, AbstractUser, Group
from django.conf import settings
from proyectos.models import Proyectos
import uuid
import os
from django.core.files.storage import default_storage
from PIL import Image
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


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

# Generar un nombre aleatorio usando la librería uuid


def profile_picture_path(instance, filename):
    random_filename = str(uuid.uuid4())
    # recupero la extensión del archivo de imagen
    extension = os.path.splitext(filename)[1]
    return 'users/{0}/{1}{2}'.format(instance.user, random_filename, extension)


class Usuario(models.Model):  # class User(AbstractUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=profile_picture_path, blank=True)
    birthday = models.DateField(null=True, blank=True)
    dark_mode = models.BooleanField(default=False)
    telefono = models.CharField(
        max_length=20, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if self.pk and self.image != None:
            old_profile = Usuario.objects.get(pk=self.pk) if self.pk else None
            if old_profile.image and old_profile.image.path != self.image.path:
                default_storage.delete(old_profile.image.path)
        super(Usuario, self).save(*args, **kwargs)

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


@receiver(post_save, sender=User)
def create_usuario(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(user=instance)


class Reporte_tarea(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    proyecto = models.ForeignKey(
        Proyectos, on_delete=models.CASCADE, default=None, blank=True, null=True)
    informe = models.CharField(max_length=1000)
