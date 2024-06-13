import random
import string
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.models import User

# Función que genera una contraseña aleatoria de 10 caracteres para que el usuario pueda ingresar
# cuando se ha olvidado su contraseña y una vez adentro, pueda acceder a cambiarla.


def generar_contrasena():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for _ in range(10))
    return contrasena


def notificar_contrasena(correo, usuario, contrasena):

    # tarea = Tareas.objects.get(id=tarea_id)
    # correo_encargado = User.objects.get(username=tarea.encargado).email
    # url_tarea = f'https://{settings.ALLOWED_HOSTS[0]}/core/explorarTarea/{tarea.nombre}'
    template = get_template('core/correo_contrasena.html')
    data = {
        'usuario': usuario,
        'contrasena': contrasena,
    }
    content = template.render(data)

    email = EmailMultiAlternatives(
        'Nueva contraseña.',
        'Se ha solicitado restablecer la contraseña de esta cuenta.',
        'gerencia@connelec.com.ar',
        [correo],
    )

    email.attach_alternative(content, 'text/html')
    email.send()
