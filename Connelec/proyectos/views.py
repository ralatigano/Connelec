from django.shortcuts import render, redirect
from clientes.models import Cliente
from .models import Proyectos
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# cambio esto para probar un modelo de usuario con una aplicación OneToOneField con User
from django.contrib.auth.models import User
# from asistencias.models import User

app_name = 'proyectos'


@login_required
def proyectos(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=request.user).get_full_name()
        img = User.objects.get(username=request.user).usuario.image.url
        data = {
            'usuario': usuario,
            'img': img
        }
    return render(request, 'proyectos/proyectos.html', data)


@login_required
def ver_proyectos(request):
    usuario = User.objects.get(username=request.user).get_full_name()
    Usus = User.objects.all()
    Proys = Proyectos.objects.all()
    data = {
        'usuario': usuario,
        'Usus': Usus,
        'Proys': Proys
    }
    return render(request, 'proyectos/ver_proyectos.html', data)


@login_required
def crear_proyecto(request):
    usuario = User.objects.get(username=request.user).get_full_name()
    Usus = User.objects.all()
    if request.method == 'POST':
        try:
            Proyectos.objects.create(
                nombre=request.POST['nombre'],
                descripcion=request.POST['descripcion'],
                cliente=Cliente.objects.get(nombre=request.POST['cliente'])
            )
            messages.success(request, 'Proyecto creado con exito.')
        except Exception as e:
            messages.error(
                request, 'Hubo un error al crear el proyecto: ' + str(e) + '.')
        return redirect('verProyectos')
    if request.user.is_authenticated:
        Clies = Cliente.objects.all()
        data = {
            'usuario': usuario,
            'Usus': Usus,
            'Clies': Clies
        }
    return render(request, 'proyectos/crear_proyecto.html', data)


@login_required
def editar_proyecto(request):
    try:
        p = Proyectos.objects.get(nombre=request.POST['nombre'])
        if request.POST['n_expediente'] and p.n_expediente != request.POST['n_expediente']:
            p.n_expediente = request.POST['n_expediente']
            p.save()
            messages.success(request, 'Proyecto editado con exito.')
    except Exception as e:
        messages.error(
            request, 'Hubo un error al editar el proyecto: ' + str(e) + '.')

    return redirect('verProyectos')
