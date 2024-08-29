from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from .functions import *
from .models import Usuario, AusenciaJustificada
import os
from django.conf import settings
from PIL import Image
import random


@receiver(post_save, sender=User)
def create_usuario(sender, instance, created, **kwargs):
    if created:
        usuario = Usuario.objects.create(user=instance)
        base_image_path = os.path.join(
            settings.MEDIA_ROOT + '/users/', 'default.png')
        random_image = generate_random_color_image(base_image_path)
        image_path = profile_picture_path(usuario, 'profile.png')
        full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
        os.makedirs(os.path.dirname(full_image_path), exist_ok=True)
        random_image.save(full_image_path)
        usuario.image = image_path
        usuario.save()


@receiver(post_delete, sender=AusenciaJustificada)
def delete_archivo_on_delete(sender, instance, **kwargs):
    if instance.archivo:
        archivo_path = instance.archivo.path
        if instance.archivo and default_storage.exists(archivo_path):
            default_storage.delete(archivo_path)


def generate_random_color_image(base_image_path, size=(300, 300)):
    color = tuple(random.randint(0, 255) for _ in range(3))
    background = Image.new('RGBA', size, color)
    base_image = Image.open(base_image_path).convert('RGBA')
    base_image.thumbnail(size, Image.LANCZOS)
    background.paste(base_image, (0, 0), base_image)
    return background
