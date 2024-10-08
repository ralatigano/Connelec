from django.shortcuts import render
from django.template.loader import get_template
from .models import Tareas
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
# cambio esto para probar un modelo de usuario con una aplicación OneToOneField con User
from django.contrib.auth.models import User
# from asistencias.models import User


def notificar_encargado(tarea_id, usuario):

    tarea = Tareas.objects.get(id=tarea_id)
    correo_encargado = User.objects.get(username=tarea.encargado).email
    url_tarea = f'https://{settings.ALLOWED_HOSTS[0]}/tareas/explorarTarea/{tarea.nombre}'
    template = get_template('tareas/tarea_correo.html')
    data = {
        'usuario': usuario,
        'tarea_nombre': tarea.nombre,
        'tarea_descrip': tarea.descrip,
        'tarea_encargado': tarea.encargado,
        'tarea_proyecto': tarea.proyecto,
        'tarea_fecha_entrega': tarea.fecha_entrega,
        'url_tarea': url_tarea
    }
    content = template.render(data)

    email = EmailMultiAlternatives(
        'Nueva tarea asignada.',
        'Le han asignado una nueva tarea.',
        'gerencia@connelec.com.ar',
        [correo_encargado],
    )

    email.attach_alternative(content, 'text/html')
    email.send()
