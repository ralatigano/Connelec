from django.shortcuts import render, redirect
from asistencias.models import User
from .models import Cliente
from django.contrib import messages


app_name = 'clientes'

def clientes(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=request.user).get_full_name()
        img = User.objects.get(username=request.user).image.url
        data = {
            'usuario': usuario,
            'img': img
        }
    return render(request, 'clientes/clientes.html', data)

def ver_clientes(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=request.user).get_full_name()
        Clies = Cliente.objects.all()
        data = {
            'usuario': usuario,
            'Clies': Clies
        }
    return render(request, 'clientes/ver_clientes.html', data)

def nuevo_cliente(request):
    if request.method == 'POST':
        try:
            Cliente.objects.create(
                nombre = request.POST['nombre'],
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
        except Exception as e:
            messages.error(request, 'Hubo un error al crear el cliente: ' + str(e) + '.')
    
    return render(request, 'clientes/nuevo_cliente.html')


def editar_cliente(request):
    if request.method == 'POST':
        try:
            cli = Cliente.objects.get(nombre = request.POST['nombre'])
            if request.POST['razon_social'] != cli.razon_social:
                cli.razon_social = request.POST['razon_social']
            if request.POST['cuit'] != cli.cuit:
                cli.cuit = request.POST['cuit']
            if request.POST['email'] != cli.email:
                cli.email = request.POST['email']
            if request.POST['telefono'] != cli.telefono:
                cli.telefono = request.POST['telefono']
            if request.POST['direccion'] != cli.direccion:
                cli.direccion = request.POST['direccion']
            if request.POST['provincia'] != 'Otra región':
                cli.provincia = request.POST['provincia']
            cli.save()
            messages.success(request, 'Cliente editado con exito.')
        except Exception as e:
            messages.error(request, 'Hubo un error al editar el cliente: ' + str(e) + '.')
    
    return redirect('ver_clientes')
