from django.shortcuts import render, redirect
from .models import Cliente
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# cambio esto para probar un modelo de usuario con una aplicación OneToOneField con User
# from asistencias.models import User
from django.contrib.auth.models import User

app_name = 'clientes'

# Menu clientes
# Junta el contexto en la variable data y lo pasa al render. Se evalua los permisos del usuario
# para habilitar ciertas funciones o incluso ocultar algunos elementos del template.


@login_required
def clientes(request):
    crear = False
    if request.user.has_perm('clientes.add_cliente'):
        crear = True
    usuario = User.objects.get(username=request.user).get_full_name()
    img = User.objects.get(username=request.user).usuario.image.url
    data = {
        'usuario': usuario,
        'img': img,
        'crear': crear,
    }
    return render(request, 'clientes/clientes.html', data)

# Vista que enlista todos los clientes registrados. Se evalua si el usuario que hace la solicitud forma parte de un grupo específico
# o si es superusuario para habilitar algunas funciones o incluso mostrar algunos elementos del template.


@login_required
def ver_clientes(request):
    autorizado = False
    if request.user.groups.filter(name='Equipo Administrativo').exists() or str(request.user) == 'superusuario':
        autorizado = True
    usuario = User.objects.get(username=request.user).get_full_name()

    Clies = Cliente.objects.all()
    data = {
        'usuario': usuario,
        'Clies': Clies,
        'autorizado': autorizado,
    }
    return render(request, 'clientes/ver_clientes.html', data)

# Vista para registrar un nuevo cliente. La vista está pensada para mostrar el formulario de registro y para manejar el POST que resulta de
# de completarlo y guardarlo.


@login_required
def nuevo_cliente(request):
    desdeVerClientes = False
    if 'verClientes' in request.META.get('HTTP_REFERER'):
        desdeVerClientes = True
    if request.method == 'POST':
        try:
            Cliente.objects.create(
                nombre=request.POST['nombre'],
            )
            if request.POST['razon_social'] != '':
                cliente = Cliente.objects.last()
                cliente.razon_social = request.POST['razon_social']
                cliente.save()
            if request.POST['cuit'] != '':
                cliente = Cliente.objects.last()
                cliente.cuit = request.POST['cuit']
                cliente.save()
            if request.POST['email'] != '':
                cliente = Cliente.objects.last()
                cliente.email = request.POST['email']
                cliente.save()
            if request.POST['telefono'] != '':
                cliente = Cliente.objects.last()
                cliente.telefono = request.POST['telefono']
                cliente.save()
            if request.POST['direccion'] != '':
                cliente = Cliente.objects.last()
                cliente.direccion = request.POST['direccion']
                cliente.save()
            if request.POST['provincia'] != 'Sin asignar':
                cliente = Cliente.objects.last()
                cliente.provincia = request.POST['provincia']
                cliente.save()
            messages.success(request, 'Cliente creado con exito.')
            return redirect('ver_clientes')
        except Exception as e:
            messages.error(
                request, 'Hubo un error al crear el cliente: ' + str(e) + '.')
    else:
        usuario = User.objects.get(username=request.user).get_full_name()
        data = {
            'usuario': usuario,
            'desdeVerClientes': desdeVerClientes,
        }
        return render(request, 'clientes/nuevo_cliente.html', data)

# Vista para editar un cliente. Esta vista siempre viene de un POST porque los datos se editan en una ventana modal.


@login_required
def editar_cliente(request):

    try:
        cli = Cliente.objects.get(nombre=request.POST['nombre'])
        cambios = False
        if request.POST['razon_social'] != cli.razon_social:
            cli.razon_social = request.POST['razon_social']
            cambios = True
        if request.POST['cuit'] != cli.cuit:
            cli.cuit = request.POST['cuit']
            cambios = True
        if request.POST['email'] != cli.email:
            cli.email = request.POST['email']
            cambios = True
        if request.POST['telefono'] != cli.telefono:
            cli.telefono = request.POST['telefono']
            cambios = True
        if request.POST['direccion'] != cli.direccion:
            cli.direccion = request.POST['direccion']
            cambios = True
        if request.POST['provincia'] != 'Otra región':
            cli.provincia = request.POST['provincia']
            cambios = True
        if cambios:
            cli.save()
            messages.success(request, 'Cliente editado con exito.')
    except Exception as e:
        messages.error(
            request, 'Hubo un error al editar el cliente: ' + str(e) + '.')
    return redirect('ver_clientes')

# Vista que permite borrar un cliente.


@login_required
def borrar_cliente(request, id):
    try:
        cli = Cliente.objects.get(id=id)
        cli.delete()
        messages.success(request, 'Cliente borrado con exito.')
    except Exception as e:
        messages.error(
            request, 'Hubo un error al borrar el cliente: ' + str(e) + '.')
    return redirect('ver_clientes')
