from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from datetime import datetime, date
from .functions import *
from proyectos.models import Proyectos
from django.contrib.auth.decorators import login_required
# cambio esto para probar un modelo de usuario con una opción OneToOneField con User
from .models import registro, Reporte_tarea  # User,
from django.contrib.auth.models import User, Group

app_name = 'asistencias'
# Create your views here.

# Vista que renderiza el menú asistencia. Verifica si el usuario tiene un permiso para agregar registros
# y en función de eso modifica un booleano para mostrar o no ciertos elementos del template.
# Arma el contexto necesario en el diccionario data y lo pasa al render.


@login_required
def asistencia(request):
    crear = False
    if request.user.has_perm('asistencias.add_registro'):
        crear = True
    usuario = User.objects.get(username=request.user).get_full_name()
    img = User.objects.get(username=request.user).usuario.image.url
    data = {
        'usuario': usuario,
        'img': img,
        'crear': crear,
    }
    return render(request, 'asistencias/asistencia.html', data)

# Vista que le permite al usuario calcular el tiempo que lleva trabajado durante la jornada.
# Cabe aclarar que por la lógica de la aplicación, el cálculo se hace entre una marca de entrada y la hora actual.


@login_required
def hoy(request):
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
        'mensaje': mensaje,
    }
    return render(request, 'asistencias/hoy.html', data)

# Vista que permite calcular las horas trabajadas en un rango de fechas. La vista está pensada para renderizar
# el template inicial y para procesar la devolución. Prepara el contexto en la variable data en donde lleva un booleano
# que indica si el usuario es capaz de calcular las horas de cualquier persona o si solo puede calcular las suyas.


@login_required
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

    usuario = User.objects.get(username=username).get_full_name()
    autorizado = False
    grupos_con_permiso = ['Gerencia', 'Jefe Area']
    if any(username.groups.filter(name=grupo).exists() for grupo in grupos_con_permiso):
        autorizado = True
    data = {
        'usuario': usuario,
        'username': username,
        'Usus': Usus,
        'autorizado': autorizado,
    }
    return render(request, 'asistencias/ver_periodo.html', data)

# Registros

# Vista que permite al usuario registrar SU entrada o salida. No puede cargar la de otro usuario.


@login_required
def marcar_asistencia(request):
    desdeRegistros = False
    desdeHoy = False
    if 'verAsistencias' in request.META.get('HTTP_REFERER'):
        desdeRegistros = True
    if 'hoy' in request.META.get('HTTP_REFERER'):
        desdeHoy = True
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
        return redirect('verAsistencias')
    Usus = User.objects.all()
    username = request.user
    autorizado = False
    if str(username) == 'superusuario':
        autorizado = True
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
        'ult_reg': ult_reg,
        'autorizado': autorizado,
        'desdeRegistros': desdeRegistros,
        'desdeHoy': desdeHoy,
    }
    return render(request, 'asistencias/marcar_asistencia.html', data)

# Vista para ver todos los registros de asistencias de todos los usuarios.
# Se evalua los permisos del usuario que hace la solicitud para habilitar ciertas funciones
# o incluso ocultar algunos elementos del template.


@login_required
def listar_registros(request):
    crear = False
    editar = False
    borrar = False
    if request.user.has_perm('asistencias.add_registro'):
        crear = True
    if request.user.has_perm('asistencias.change_registro'):
        editar = True
    if request.user.has_perm('asistencias.delete_registro'):
        borrar = True

    usuario = User.objects.get(username=request.user).get_full_name()
    registros = registro.objects.all()
    data = {
        'usuario': usuario,
        'registros': registros,
        'crear': crear,
        'borrar': borrar,
        'editar': editar,
    }
    return render(request, 'asistencias/registros.html', data)

# Vista que permite la edición de un registro de asistencia. Esta vista siempre es
# llamada por un formulario que trae un POST con la información por eso no lleva la verificación.


@login_required
def editar_registro(request):
    try:
        reg = registro.objects.get(id=request.POST['id'])
        cambios = False
        if request.POST['fecha'] != reg.fecha:
            reg.fecha = request.POST['fecha']
            cambios = True
        if request.POST['hora'] != reg.hora:
            reg.hora = request.POST['hora']
            cambios = True
        if request.POST['tipo'] != reg.tipo:
            reg.tipo = request.POST['tipo']
            cambios = True
        if cambios:
            reg.save()
            messages.success(request, "Registro editado con exito.")
    except Exception as e:
        messages.error(
            request, "Hubo un error al editar el registro: " + str(e) + ".")
    return redirect('verAsistencias')

# Vista que permite el borrado de un registro de asistencia.


@login_required
def borrar_registro(request, id):
    try:
        reg = registro.objects.get(id=id)
        reg.delete()
        messages.success(request, "Registro borrado con exito.")
    except Exception as e:
        messages.error(
            request, "Hubo un error al borrar el registro: " + str(e) + ".")
    return redirect('verAsistencias')

# Menu Reportes
# Se evalua el permiso de creación para ocultar el botón de crear un nuevo reporte.


@login_required
def reportes(request):
    crear = False
    if request.user.has_perm('asistencias.add_registro'):
        crear = True
    usuario = User.objects.get(username=request.user).get_full_name()
    img = User.objects.get(username=request.user).usuario.image.url
    data = {
        'usuario': usuario,
        'img': img,
        'crear': crear,
    }
    return render(request, 'asistencias/reportes.html', data)

# Vista que lista todos los reportes de las tareas realizadas en el día por el personal.
# Se evaluan los permisos del usuario que ingresa a la vista de modo de limitar ciertas acciones como editar o borrar registros
# o incluso la creación de uno nuevo.


@login_required
def ver_reportes(request):
    crear = False
    editar = False
    borrar = False
    if request.user.has_perm('asistencias.add_reporte_tarea'):
        crear = True
    if request.user.has_perm('asistencias.change_reporte_tarea'):
        editar = True
    if request.user.has_perm('asistencias.delete_reporte_tarea'):
        borrar = True
    usuario = User.objects.get(username=request.user).get_full_name()
    reportes = Reporte_tarea.objects.all()
    data = {
        'usuario': usuario,
        'reportes': reportes,
        'crear': crear,
        'borrar': borrar,
        'editar': editar,
    }
    return render(request, 'asistencias/ver_reportes.html', data)

# Vista para crear reportes. Está pensada para procesar la creación de un nuevo reporte y
# recibir la información una vez que se completa el formulario.


@login_required
def crear_reporte(request):
    desdeReportes = False
    if 'verReportes' in request.META.get('HTTP_REFERER'):
        desdeReportes = True
    if request.method == 'POST':
        # if request.POST["usuario"] == request.user and request.POST['fecha'] <= date.today().strftime("%Y-%m-%d") and request.POST['hora'] <= datetime.now().time():
        try:
            Reporte_tarea.objects.create(
                usuario=User.objects.get(username=request.POST['usuario']),
                informe=request.POST['informe'],
                fecha=request.POST['fecha'],
                hora=request.POST['hora'],
            )
            if request.POST['proyecto'] != 'Ninguno':
                r = Reporte_tarea.objects.last()
                r.proyecto = Proyectos.objects.get(
                    nombre=request.POST['proyecto'])
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
            'Proys': Proys,
            'desdeReportes': desdeReportes,
        }
        return render(request, 'asistencias/nuevo_reporte.html', data)

# Vista para editar un reporte diario. Esta vista siempre es
# llamada por un formulario que trae un POST con la información por eso no lleva la verificación.


@login_required
def editar_reporte(request):
    try:
        r = Reporte_tarea.objects.get(id=request.POST['id'])
        cambios = False
        if request.POST['informe'] != r.informe:
            r.informe = request.POST['informe']
            cambios = True
        if request.POST['fecha'] != r.fecha:
            r.fecha = request.POST['fecha']
            cambios = True
        if request.POST['hora'] != r.hora:
            r.hora = request.POST['hora']
            cambios = True
        if request.POST['proyecto'] == 'Ninguno':
            r.proyecto = None
        else:
            if request.POST['proyecto'] != r.proyecto:
                r.proyecto = Proyectos.objects.get(
                    nombre=request.POST['proyecto'])
                cambios = True
        if cambios:
            r.save()
            messages.success(request, 'Reporte editado con exito.')
    except Exception as e:
        messages.error(
            request, 'Hubo un error al editar el reporte: ' + str(e) + '.')
    return redirect('verReportes')

# Vista que permite el borrado de un reporte.


@login_required
def borrar_reporte(request, id):
    try:
        r = Reporte_tarea.objects.get(id=id)
        r.delete()
        messages.success(request, 'Reporte borrado con exito.')
    except Exception as e:
        messages.error(
            request, 'Hubo un error al borrar el reporte: ' + str(e) + '.')
    return redirect('verReportes')
