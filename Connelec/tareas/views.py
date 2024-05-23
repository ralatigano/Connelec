from django.shortcuts import render, redirect
from asistencias.models import User
from .models import Tareas, Archivos, Entrada_historial
from django.contrib import messages
from proyectos.models import Proyectos
from datetime import datetime
from django.http import JsonResponse
from django.core import serializers
from .functions import *


app_name = 'tareas'

# Create your views here.


def tareas(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=request.user).get_full_name()
        img = User.objects.get(username=request.user).image.url
        data = {
            'usuario': usuario,
            'img': img
        }
    return render(request, 'tareas/tareas.html', data)


def ver_tareas(request):
    usuario = User.objects.get(username=request.user).get_full_name()
    Tars = Tareas.objects.all().order_by('-fecha_creacion')
    data = {
        'usuario': usuario,
        'Tars': Tars,
    }
    return render(request, 'tareas/ver_tareas.html', data)


def ver_mis_tareas(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=request.user).get_full_name()
        Tars = Tareas.objects.filter(
            encargado=request.user).order_by('-fecha_creacion')
        data = {
            'usuario': usuario,
            'Tars': Tars,
        }
    return render(request, 'tareas/ver_mis_tareas.html', data)


def crear_tarea(request):
    usuario = User.objects.get(username=request.user).get_full_name()
    Usus = User.objects.all()
    Proys = Proyectos.objects.all()
    if request.method == 'POST':
        try:
            Tareas.objects.create(
                nombre=request.POST['nombre'],
                descrip=request.POST['descripcion'],
                fecha_entrega=None,
                estado=request.POST['estado'],
                proyecto=None,
                encargado=None
            )
            if request.POST['fecha_entrega'] == 'dd/mm/aaaa':
                tarea = Tareas.objects.last()
                tarea.fecha_entrega = request.POST['fecha_entrega']
                tarea.save()
            if request.POST['proyecto'] != 'Ninguno':
                tarea = Tareas.objects.last()
                tarea.proyecto = Proyectos.objects.get(
                    nombre=request.POST['proyecto'])
                tarea.save()
            if request.POST['encargado'] != 'Ninguno':
                tarea = Tareas.objects.last()
                tarea.encargado = User.objects.get(
                    username=request.POST['encargado'])
                tarea.save()
                # Si hay un asignado, me interesa notificarlo.
                usuario = request.user
                tarea_id = tarea.id

                notificar_encargado(tarea_id, usuario)
            if request.FILES:
                for archivo in request.FILES.getlist('adjunto'):
                    Archivos.objects.create(
                        nombre=archivo.name,
                        tarea=Tareas.objects.last(),
                        archivo=archivo
                    )

            messages.success(request, 'Tarea creada con exito.')
        except Exception as e:
            messages.error(
                request, 'Hubo un error al crear la tarea: ' + str(e) + '.')
        return redirect('verTareas')
    if request.user.is_authenticated:
        data = {
            'usuario': usuario,
            'Usus': Usus,
            'Proys': Proys
        }
    return render(request, 'tareas/crear_tarea.html', data)


def info_editar_tarea(request):
    Usus = User.objects.all()
    Proys = Proyectos.objects.all()

    Usus_data = list(Usus.values('id', 'username', 'first_name', 'last_name'))
    Proys_data = list(Proys.values('nombre'))
    data = {
        'Usus': Usus_data,
        'Proys': Proys_data
    }
    return JsonResponse(data)


def editar_tarea(request):
    if request.method == 'POST':
        try:
            tarea = Tareas.objects.get(nombre=request.POST['nombre'])
            if tarea.descrip != request.POST['descrip'] and request.POST['descrip'] != '':
                tarea.descrip = request.POST['descrip']

            if tarea.encargado != request.POST['encargado']:
                if request.POST['encargado'] == 'Ninguno':
                    tarea.encargado = None
                else:
                    tarea.encargado = User.objects.get(
                        username=request.POST['encargado'])
            if tarea.proyecto != request.POST['proyecto']:
                if request.POST['proyecto'] == 'Ninguno':
                    tarea.proyecto = None
                else:
                    tarea.proyecto = Proyectos.objects.get(
                        nombre=request.POST['proyecto'])
            if tarea.estado != request.POST['estado']:
                tarea.estado = request.POST['estado']
            if tarea.fecha_entrega != request.POST['fecha_entrega']:
                if request.POST['fecha_entrega'] == '':
                    tarea.fecha_entrega = None
                else:
                    tarea.fecha_entrega = request.POST['fecha_entrega']
            if request.FILES:
                for archivo in request.FILES.getlist('adjunto'):
                    Archivos.objects.create(
                        nombre=archivo.name,
                        tarea=Tareas.objects.get(id=tarea.id),
                        archivo=archivo
                    )
            tarea.save()
            messages.success(request, 'Tarea editada con exito.')
        except Exception as e:
            messages.error(
                request, 'Hubo un error al editar la tarea: ' + str(e) + '.')
    return redirect('verTareas')


def tareas_asosc_proy(request, proy):
    usuario = User.objects.get(username=request.user).get_full_name()
    Usus = User.objects.all()
    p = Proyectos.objects.get(nombre=proy).id
    Tars = Tareas.objects.filter(proyecto=p)
    data = {
        'usuario': usuario,
        'Usus': Usus,
        'Tars': Tars,
    }
    return render(request, 'tareas/tareas_asoc_proyecto.html', data)


def explorar_tarea(request, nombTarea):
    usuario = User.objects.get(username=request.user).get_full_name()
    Usus = User.objects.all()
    try:
        Tarea = Tareas.objects.get(nombre=nombTarea)
        Files = Archivos.objects.filter(tarea=Tarea.id)
        data = {
            'usuario': usuario,
            'Usus': Usus,
            'Tarea': Tarea,
            'Files': Files
        }
    except Exception as e:
        messages.error(
            request, 'Hubo un error al recuperar la información de la tarea: ' + str(e) + '.')
    return render(request, 'tareas/explorar.html', data)


def entradas_asosc_proy(request, proy):

    usuario = User.objects.get(username=request.user).get_full_name()
    Usus = User.objects.all()
    p = Proyectos.objects.get(nombre=proy).id
    n_expediente = Proyectos.objects.get(nombre=proy).n_expediente
    Entries = Entrada_historial.objects.filter(proyecto=p)
    data = {
        'usuario': usuario,
        'Usus': Usus,
        'proyecto': proy,
        'n_expediente': n_expediente,
        'Entries': Entries,
    }
    return render(request, 'tareas/entradas_asoc_proyecto.html', data)


def crear_entrada(request, proy):
    if request.method == 'POST':
        try:
            Entrada_historial.objects.create(
                fecha=request.POST['fecha'],
                resumen=request.POST['resumen'],
                proyecto=Proyectos.objects.get(
                    nombre=request.POST['proyecto']),
                usuario=request.user)
            if request.FILES:
                ent = Entrada_historial.objects.last()
                ent.adjunto = request.FILES['adjunto']
                ent.save()
            messages.success(request, 'Entrada creada con exito.')
        except Exception as e:
            messages.error(
                request, 'Hubo un error al crear la entrada: ' + str(e) + '.')
        return redirect('entradasAsocProyecto', proy=request.POST['proyecto'])
    else:
        usuario = User.objects.get(username=request.user).get_full_name()
        Usus = User.objects.all()
        Proys = Proyectos.objects.all()
        data = {
            'usuario': usuario,
            'Usus': Usus,
            'proyecto': proy,
            'Proys': Proys,
        }
        return render(request, 'tareas/crear_entrada.html', data)
