from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from .models import User, registro, Reporte
from datetime import datetime, date
from .functions import *
from proyectos.models import Proyectos


app_name = 'asistencias'
# Create your views here.


def asistencia(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=request.user).get_full_name()
        img = User.objects.get(username=request.user).image.url
        data = {
            'usuario': usuario,
            'img': img
        }
    return render(request, 'asistencias/asistencia.html', data)


def hoy(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=request.user).get_full_name()
        id = User.objects.get(username=request.user).id
        fecha = date.today().strftime("%Y-%m-%d")
        registros = registro.objects.filter(fecha=fecha).filter(usuario=id)
        hora_actual = datetime.today().time()
        hora_actual_obj = datetime.strptime(
            str(hora_actual.hour)+':'+str(hora_actual.minute), '%H:%M')
        if len(registros) > 0:
            tiempo = calcular_horas_totales_hoy(registros, hora_actual_obj)
            mensaje = f'Usted trabajó {tiempo} horas el dia de hoy.'
        else:
            mensaje = 'Todavía no se ha registrado una entrada para el día de hoy.'
        data = {
            'usuario': usuario,
            'fecha': fecha,
            'mensaje': mensaje
        }
    return render(request, 'asistencias/hoy.html', data)


def ver_periodo(request):
    Usus = User.objects.all()
    username = request.user
    if request.method == 'POST':
        usuario = request.POST['usuario']
        u_id = User.objects.get(username=usuario)
        fecha1_str = request.POST['fecha1']
        fecha1_obj = datetime.strptime(fecha1_str, '%Y-%m-%d')
        fecha2_str = request.POST['fecha2']
        fecha2_obj = datetime.strptime(fecha2_str, '%Y-%m-%d')
        mensaje = []
        mensaje = Calcular_horas(fecha1_obj, fecha2_obj, u_id)
        data = {
            'usuario': usuario,
            'username': username,
            'Usus': Usus,
        }
        if mensaje[1] == True:
            messages.error(request, mensaje[0])
        else:
            messages.success(request, mensaje[0])
        return render(request, 'asistencias/ver_periodo.html', data)

    if request.user.is_authenticated:
        usuario = User.objects.get(username=username).get_full_name()
        data = {
            'usuario': usuario,
            'username': username,
            'Usus': Usus,
        }
        return render(request, 'asistencias/ver_periodo.html', data)


def marcar_asistencia(request):
    if request.method == 'POST':
        try:
            usuario = request.POST['usuario']
            fecha_str = request.POST['fecha']
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
            hora = request.POST['hora']
            tipo = request.POST['tipo']
            registro.objects.create(
                usuario=User.objects.get(username=usuario),
                fecha=fecha_obj,
                hora=hora,
                tipo=tipo
            )
            messages.success(request, 'Asistencia registrada con exito.')
        except Exception as e:
            messages.error(
                request, 'Hubo un error al registrar la asistencia: ' + str(e) + '.')

    if request.user.is_authenticated:
        Usus = User.objects.all()
        username = request.user
        usuario = User.objects.get(username=username).get_full_name()
        user_id = User.objects.get(username=username).id
        fecha_guion = date.today().strftime("%Y-%m-%d")
        hora = datetime.now().time()
        # obtengo el último registro del usuario en el día de la fecha de modo de que el formulario induzca a marcar una entrada o salida según que sea lo último que se registró.
        try:
            ult_reg = registro.objects.filter(
                fecha=fecha_guion).filter(usuario=user_id).last().tipo
        except:
            ult_reg = None
        data = {
            'usuario': usuario,
            'username': username,
            'Usus': Usus,
            'fecha': fecha_guion,
            'hora': hora,
            'ult_reg': ult_reg
        }
    return render(request, 'asistencias/marcar_asistencia.html', data)


def listar_registros(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=request.user).get_full_name()
        registros = registro.objects.all()
        data = {
            'usuario': usuario,
            'registros': registros
        }
    return render(request, 'asistencias/registros.html', data)


def reportes(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=request.user).get_full_name()
        img = User.objects.get(username=request.user).image.url
        data = {
            'usuario': usuario,
            'img': img
        }
    return render(request, 'asistencias/reportes.html', data)


def ver_reportes(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=request.user).get_full_name()
        reportes = Reporte.objects.all()
        data = {
            'usuario': usuario,
            'reportes': reportes
        }
    return render(request, 'asistencias/ver_reportes.html', data)


def crear_reporte(request):
    if request.method == 'POST':
        try:
            Reporte.objects.create(
                usuario=User.objects.get(username=request.POST['usuario']),
                informe=request.POST['informe'],
                fecha=request.POST['fecha'],
                hora=request.POST['hora'],
                proyecto=None
            )
            if request.POST['proyecto'] != 'Ninguno':
                r = Reporte.objects.last()
                r.proyecto = request.POST['proyecto']
                r.save()
            messages.success(request, 'Reporte creado con exito.')
        except Exception as e:
            messages.error(
                request, 'Hubo un error al crear el reporte: ' + str(e) + '.')
        return redirect('verReportes')
    else:
        nombre_usuario = request.user
        usuario = User.objects.get(username=request.user).get_full_name()
        fecha = date.today().strftime("%Y-%m-%d")
        hora = datetime.now().time()
        Proys = Proyectos.objects.all()
        data = {
            'usuario': usuario,
            'nombre_usuario': nombre_usuario,
            'fecha': fecha,
            'hora': hora,
            'Proys': Proys
        }
        return render(request, 'asistencias/nuevo_reporte.html', data)


def editar_reporte(request):
    try:
        r = Reporte.objects.get(id=request.POST['id'])
        if request.POST['proyecto'] == 'Ninguno':
            r.proyecto = None
        else:
            r.proyecto = Proyectos.objects.get(nombre=request.POST['proyecto'])
        r.save()
        messages.success(request, 'Reporte editado con exito.')
    except Exception as e:
        messages.error(
            request, 'Hubo un error al editar el reporte: ' + str(e) + '.')
    return redirect('verReportes')
