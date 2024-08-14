from django.shortcuts import render, redirect
from clientes.models import Cliente
from .models import Proyectos
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# cambio esto para probar un modelo de usuario con una aplicación OneToOneField con User
from django.contrib.auth.models import User
# from asistencias.models import User

app_name = 'proyectos'

# Menu proyectos. Se evalúan los permisos del usuario que realiza la solicitud para habilitar ciertas funciones
# o incluso ocultar algunos elementos del template.


@login_required
def proyectos(request):
    crear = False
    if request.user.has_perm('proyectos.add_proyectos'):
        crear = True
    usuario = User.objects.get(username=request.user).get_full_name()
    img = User.objects.get(username=request.user).usuario.image.url
    data = {
        'usuario': usuario,
        'img': img,
        'crear': crear,
    }
    return render(request, 'proyectos/proyectos.html', data)

# Vista que enlista todos los proyectos registrados. Se evalua si el usuario que hace la solicitud forma parte de un grupo específico
# o si es superusuario para habilitar algunas funciones o incluso mostrar algunos elementos del template.


@login_required
def ver_proyectos(request):
    autorizado = False
    # menu_secundario = request.session['url_anterior'] = request.META.get(
    #     'HTTP_REFERER')
    if request.user.groups.filter(name='Jefe Area').exists() or str(request.user) == 'superusuario':
        autorizado = True
    usuario = User.objects.get(username=request.user).get_full_name()
    Usus = User.objects.all()
    Proys = Proyectos.objects.all()
    data = {
        'usuario': usuario,
        'Usus': Usus,
        'Proys': Proys,
        'autorizado': autorizado,
        # 'menu_secundario': menu_secundario,
    }
    return render(request, 'proyectos/ver_proyectos.html', data)

# Vista que permite la creación de un proyecto. La vista está pensada para mostrar el formulario de creación y para manejar el POST que resulta de
# de completarlo y guardarlo.


@login_required
def crear_proyecto(request):
    desdeVerProyectos = False
    if 'verProyectos' in request.META.get('HTTP_REFERER'):
        desdeVerProyectos = True
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
            'Clies': Clies,
            'desdeVerProyectos': desdeVerProyectos,
        }
    return render(request, 'proyectos/crear_proyecto.html', data)

# Viista que es llamada desde una solicitud AJAX para tener la información de los clientes en formato JSON.


@login_required
def info_editar_proyecto(request):
    Cli = Cliente.objects.all()

    Cli_data = list(Cli.values('id', 'nombre'))
    data = {
        'Cli': Cli_data
    }
    return JsonResponse(data)

# Vista que permite la edición de un proyecto. La información viene de un modal por lo que siempre llega a traves de un POST
# y no necesita comprobación.


@login_required
def editar_proyecto(request):
    try:
        p = Proyectos.objects.get(nombre=request.POST['nombre'])
        cli = Cliente.objects.get(id=request.POST['cliente'])
        cambios = False
        if request.POST['descripcion'] != p.descripcion:
            p.descripcion = request.POST['descripcion']
            cambios = True
        if cli.nombre != p.cliente:
            p.cliente = cli
            cambios = True
        if request.POST['n_expediente'] and p.n_expediente != request.POST['n_expediente']:
            p.n_expediente = request.POST['n_expediente']
            cambios = True
        if cambios:
            p.save()
            messages.success(request, 'Proyecto editado con exito.')
    except Exception as e:
        messages.error(
            request, 'Hubo un error al editar el proyecto: ' + str(e) + '.')

    return redirect('verProyectos')

# Vista que permite la borrar un proyecto a traves de su id.


@login_required
def borrar_proyecto(request, id):
    try:
        p = Proyectos.objects.get(id=id)
        p.delete()
        messages.success(request, 'Proyecto borrado con exito.')
    except Exception as e:
        messages.error(
            request, 'Hubo un error al borrar el proyecto: ' + str(e) + '.')

    return redirect('verProyectos')
