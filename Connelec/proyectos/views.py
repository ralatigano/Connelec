from django.shortcuts import render, redirect
from asistencias.models import User
from clientes.models import Cliente
from .models import Proyectos
from django.contrib import messages


app_name = 'proyectos'


def proyectos(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=request.user).get_full_name()
        img = User.objects.get(username=request.user).image.url
        data = {
            'usuario': usuario,
            'img': img
        }
    return render(request, 'proyectos/proyectos.html', data)


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
            # if request.POST['cliente'] != 'Ninguno':
            #    pro = Proyectos.objects.last()
            #    try:
            #        pro.cliente = Cliente.objects.get(nombre=request.POST['cliente'])
            #        pro.save()
            #    except Exception as e:
            #        messages.error(request, 'Hubo un error al intentar asignar el proyecto a el cliente: ' + str(e) + '.')
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


def editar_proyecto(request):

    try:
        p = Proyectos.objects.get(nombre=request.POST['nombre'])
        if p.n_expediente != None and p.n_expediente != request.POST['n_expediente']:
            p.n_expediente = request.POST['n_expediente']
        p.save()
        messages.success(request, 'Proyecto editado con exito.')
    except Exception as e:
        messages.error(
            request, 'Hubo un error al editar el proyecto: ' + str(e) + '.')

    return redirect('verProyectos')
