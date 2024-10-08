from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .functions import *
# cambio esto para probar un modelo de usuario con una aplicación OneToOneField con User
from django.contrib.auth.models import User
from asistencias.models import Usuario
# Create your views here.


def registrarse(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(
                request, f'Usuario {username} creado exitosamente.')
            login(request, form.get_user())
            return redirect('inicio')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            return render(request, 'core/registrarse.html', {'form': form})
    else:
        form = UserRegisterForm()
        ctx = {'form': form}
        return render(request, 'core/registrarse.html', ctx)


@login_required
def inicio(request):
    # if request.user.is_authenticated:
    usuario = User.objects.get(username=request.user).get_full_name()
    try:
        img = User.objects.get(username=request.user).usuario.image.url
        data = {
            'usuario': usuario,
            'img': img
        }
    except:
        data = {'usuario': usuario}
    return render(request, 'core/inicio.html', data)


def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        username = request.user
        try:
            info_usuario = User.objects.get(username=username)
            if request.POST['nombre'] != info_usuario.first_name:
                info_usuario.first_name = request.POST['nombre']
            if request.POST['apellido'] != info_usuario.last_name:
                info_usuario.last_name = request.POST['apellido']
            if request.POST['fecha_nac'] != info_usuario.usuario.birthday:
                info_usuario.usuario.birthday = request.POST['fecha_nac']
            if request.FILES:
                info_usuario.usuario.image = request.FILES['imagen_nueva']
            info_usuario.usuario.save()
            info_usuario.save()
            messages.success(request, 'Información actualizada correctamente.')
        except Exception as e:
            messages.error(
                request, 'Hubo un error al actualizar la información de perfil: ' + str(e) + '.')
        return redirect('perfil')
    else:
        username = request.user
        usuario = User.objects.get(username=username).get_full_name()
        first_name = User.objects.get(username=username).first_name
        last_name = User.objects.get(username=username).last_name
        birthday = datetime.strftime(User.objects.get(
            username=username).usuario.birthday, '%Y-%m-%d')
        try:
            img = User.objects.get(username=request.user).usuario.image.url
        except:
            img = ''
        data = {
            'usuario': usuario,
            'first_name': first_name,
            'last_name': last_name,
            'birthday': birthday,
            'img': img
        }
        return render(request, 'core/perfil.html', data)

# Vista que permite cambiar la contraseña una vez que este ingresó a la aplicación.


@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        if request.POST['contrasena1'] == request.POST['contrasena2'] and len(request.POST['contrasena1']) >= 8:
            user = User.objects.get(username=request.user)
            user.set_password(request.POST['contrasena1'])
            user.save()
            messages.success(request, 'Contraseña cambiada correctamente.')
            return redirect('perfil')
        else:
            messages.error(
                request, 'Las contraseñas no coinciden o es demasiado corta.')
            return redirect('cambiarContrasena')
    else:
        usuario = User.objects.get(username=request.user).get_full_name()
        img = User.objects.get(username=request.user).usuario.image.url
        data = {
            'usuario': usuario,
            'img': img
        }
        return render(request, 'core/cambiar_contrasena.html', data)

# Vista que permite restablecer la contraseña en caso de olvido.


def restablecer_contrasena(request):
    return render(request, 'core/restablecer_contrasena.html')


def correo_contrasena(request):
    usuario = request.POST['usuario']
    # print(usuario)
    email = request.POST['email']
    # print(email)
    try:
        user = User.objects.get(username=usuario)
        if user.email == email:
            contrasena_temp = generar_contrasena()
            user.set_password(contrasena_temp)
            user.save()
            # print('llega hasta aquí')
            notificar_contrasena(email, usuario, contrasena_temp)
            messages.success(
                request, 'Se ha generado una contraseña temporal y se ha enviado al correo electrónico suministrado.')
        else:
            messages.error(
                request, 'El usuario no coincide con el correo suministrado.')
    except Exception as e:
        messages.error(
            request, 'El nombre de usuario es incorrecto. ' + str(e) + '.')
    return redirect('login')

  # Vista que almacena la preferencia del usuario en relación al tema claro u oscuro de modo que
  # este se ajuste en cualquier dispositivo donde se loguee el usuario.


@login_required
def dark_mode(request, tema):

    usuario = Usuario.objects.get(user=request.user)
    if tema == 'light':
        usuario.dark_mode = False
    else:
        usuario.dark_mode = True
    usuario.save()

    request.session['url_anterior'] = request.META.get('HTTP_REFERER')
    # Redirigir al usuario a la misma página después del procesamiento
    return redirect(request.session['url_anterior'])

# Vista que pasa la preferencia de tema del usuario que se loguea.


@login_required
def get_dark_mode(request):
    usuario = Usuario.objects.get(user=request.user)
    dark_mode = 'dark' if usuario.dark_mode else 'light'
    return JsonResponse({'dark_mode': dark_mode})


def cerrar_sesion(request):
    logout(request)
    return redirect('login')
