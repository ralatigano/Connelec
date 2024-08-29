from django.db import models
# from django.contrib.auth.models import User, AbstractUser, Group
from django.conf import settings
from proyectos.models import Proyectos
import uuid
import os
from django.core.files.storage import default_storage
from PIL import Image
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import random
from datetime import timedelta

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
            self.resize_image()

    def resize_image(self):
        with Image.open(self.image.path) as img:
            ancho, alto = img.size
            if ancho > alto:
                nuevo_alto = 300
                nuevo_ancho = int((ancho/alto)*nuevo_alto)
                img = img.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
                img.save(self.image.path)
            if alto > ancho:
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

# Lógica que genera una imagen de perfil por defecto en base a la imagen default.png.


def generate_random_color_image(base_image_path, size=(300, 300)):
    color = tuple(random.randint(0, 255) for _ in range(3))
    background = Image.new('RGBA', size, color)

    base_image = Image.open(base_image_path).convert('RGBA')
    base_image.thumbnail(size, Image.LANCZOS)

    background.paste(base_image, (0, 0), base_image)
    return background

# Lógica que completa la creación de usuarios.


@receiver(post_save, sender=User)
def create_usuario(sender, instance, created, **kwargs):
    if created:
        usuario = Usuario.objects.create(user=instance)
        # Generar una imagen de perfil aleatoria con la imagen base
        base_image_path = os.path.join(
            settings.MEDIA_ROOT + '/users/', 'default.png')
        random_image = generate_random_color_image(base_image_path)
        image_path = profile_picture_path(usuario, 'profile.png')
        full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)

        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(full_image_path), exist_ok=True)

        random_image.save(full_image_path)
        usuario.image = image_path
        usuario.save()


class Reporte_tarea(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    proyecto = models.ForeignKey(
        Proyectos, on_delete=models.CASCADE, default=None, blank=True, null=True)
    informe = models.CharField(max_length=1000)


def user_ausencia_path(instance, filename):
    # Genera la ruta donde se almacenará el archivo
    random_filename = str(uuid.uuid4())
    extension = os.path.splitext(filename)[1]
    return os.path.join('users', instance.usuario.username, 'ausencias', str(instance.fecha_inicio), f'{random_filename}{extension}')


class AusenciaJustificada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.CharField(max_length=255)
    cantidad_dias = models.PositiveIntegerField()
    archivo = models.FileField(
        upload_to=user_ausencia_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:  # Si el registro ya existe
            try:
                old_record = AusenciaJustificada.objects.get(pk=self.pk)
                if old_record.archivo and old_record.archivo != self.archivo:
                    # Si el archivo ha cambiado, eliminar el antiguo
                    old_record.archivo.delete(save=False)
            except AusenciaJustificada.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ausencia de {self.usuario.username} del {self.fecha_inicio} al {self.fecha_fin}"


@receiver(post_save, sender=AusenciaJustificada)
def manage_archivos(sender, instance, created, **kwargs):
    if not created:
        # Si no es una creación, manejar la actualización
        try:
            old_instance = AusenciaJustificada.objects.get(pk=instance.pk)
            if old_instance.archivo and old_instance.archivo != instance.archivo:
                # Eliminar el archivo antiguo si ha cambiado
                if default_storage.exists(old_instance.archivo.path):
                    default_storage.delete(old_instance.archivo.path)
        except AusenciaJustificada.DoesNotExist:
            pass


@receiver(post_delete, sender=AusenciaJustificada)
def delete_archivo_on_delete(sender, instance, **kwargs):
    # Eliminar el archivo cuando se elimina la instancia
    if instance.archivo and default_storage.exists(instance.archivo.path):
        default_storage.delete(instance.archivo.path)
