from .models import registro, User
from datetime import *
from dateutil.rrule import *
from dateutil.parser import * 
import pprint
import sys
from django.contrib import messages
import calendar

jornadas = {
    'Ramiro':8,
    'Enrique':8,
    'Florencia':6,
    'Marta':5,
    'Eduardo':5,
    'Raúl':5,
    'Sarita':4
    }

def calcular_horas_totales_hoy(registros, hora_actual_obj):
    tiempo = 0
    lista_entradas = []
    lista_salidas = []
    cont_entradas = 0
    cont_salidas = 0
    tipo_reg_ant = ''
    tiempo_horas = 0
    tiempo_mins = 0
    for registro in registros:
        if registro.tipo == 'Entrada':
            #Con este if pretendo eliminar dos marcas de 'Entrada' consecutivas. Se considerará la entrada mas reciente y se sobreescribirá la anterior.
            if tipo_reg_ant != 'Entrada':
                lista_entradas.append(datetime.strptime(str(registro.hora.hour)+':'+str(registro.hora.minute),'%H:%M')) #registro.hora
                cont_entradas += 1
                tipo_reg_ant = 'Entrada'
            else:
                lista_entradas[cont_entradas] = datetime.strptime(str(registro.hora.hour)+':'+str(registro.hora.minute),'%H:%M') #registro.hora
                tipo_reg_ant = 'Entrada'
        else:
            #Con este if pretendo eliminar dos marcas de 'Salida' consecutivas. Se considerará la salida mas reciente y se sobreescribirá la anterior.
            if tipo_reg_ant != 'Salida':
                lista_salidas.append(datetime.strptime(str(registro.hora.hour)+':'+str(registro.hora.minute),'%H:%M')) #registro.hora
                cont_salidas += 1
                tipo_reg_ant = 'Salida'
            else:
                lista_salidas[cont_salidas] = datetime.strptime(str(registro.hora.hour)+':'+str(registro.hora.minute),'%H:%M') #registro.hora
                tipo_reg_ant = 'Salida'
    #Por el momento vamos a suponer que los empleados no hacen cualquiera y marcan de forma correcta las entradas y salidas, al menos en términos del orden 1ero entrada, luego salida.
    if cont_entradas > cont_salidas:
        #faltó marcar una salida.
        for i in range(cont_entradas):
            if i+1 == cont_entradas:
                tiempo_horas += (hora_actual_obj - lista_entradas[i]).total_seconds() // 3600
                tiempo_mins += (hora_actual_obj - lista_entradas[i]).total_seconds() % 3600 // 60    
            else:
                tiempo_horas += (lista_salidas[i] - lista_entradas[i]).total_seconds() // 3600
                tiempo_mins += (lista_salidas[i] - lista_entradas[i]).total_seconds() % 3600 // 60
            
    if cont_entradas == cont_salidas:
        for i in range(cont_entradas):
            tiempo_horas += (lista_salidas[i] - lista_entradas[i]).total_seconds() // 3600
            tiempo_mins += (lista_salidas[i] - lista_entradas[i]).total_seconds() % 3600 // 60
        #marcas completas.
            
    #El caso de que falte una entrada no puede darse porque se generarían dos marcas de salida consecutivas que se registrarían como 1 sola.        
    tiempo_horas = f'{tiempo_horas:.0f}'
    tiempo_mins = f'{tiempo_mins:.0f}'
    if int(tiempo_horas) < 10:
        tiempo_horas = '0'+tiempo_horas
    if int(tiempo_mins) < 10:
        tiempo_mins = '0'+tiempo_mins

    tiempo = f'{tiempo_horas}:{tiempo_mins}'
     
    return tiempo

def Calcular_horas(f1, f2, u):
    if f1 > datetime.today():
        mensaje = ['La fecha inicial no puede ser posterior al día de hoy',True]
        return mensaje
    if f2 > datetime.today():
        mensaje = ['La fecha final no puede ser posterior al día de hoy',True]
        return mensaje
    if f1 > f2:
        mensaje = ['La fecha inicial no puede ser posterior a la fecha final',True]
        return mensaje
    lista_interavalo = list(rrule(DAILY,dtstart=f1,until=f2))
    tiempo_total_horas = 0 #datetime.strptime('00:00','%H:%M')
    tiempo_total_mins = 0
    nombre = User.objects.get(username=u).get_full_name()
    for fecha in lista_interavalo:
        reg_fecha = registro.objects.filter(fecha=fecha).filter(usuario=u)
        if len(reg_fecha)>0:
            t =  Calcular_horas_totales_periodo(reg_fecha)
            tiempo_horas = t.split(':')[0]
            tiempo_mins = t.split(':')[1]
            tiempo_total_horas += int(tiempo_horas)
            tiempo_total_mins += int(tiempo_mins)
            if tiempo_total_mins >= 60:
                tiempo_total_horas += 1
                tiempo_total_mins -= 60
    tiempo_total = f'{tiempo_total_horas:.0f}:{tiempo_total_mins:.0f}'
    mensaje = [f'{nombre} trabajo {tiempo_total} horas en el periodo indicado.',False]
    return mensaje
def Calcular_horas_totales_periodo(reg_fecha):
    tiempo_horas = 0
    lista_entradas = []
    lista_salidas = []
    cont_entradas = 0
    cont_salidas = 0
    tipo_reg_ant = ''
    tiempo_horas = 0
    tiempo_mins = 0
    for registro in reg_fecha:
        if registro.tipo == 'Entrada':
            #Con este if pretendo eliminar dos marcas de 'Entrada' consecutivas. Se considerará la entrada mas reciente y se sobreescribirá la anterior.
            if tipo_reg_ant != 'Entrada':
                lista_entradas.append(datetime.strptime(str(registro.hora.hour)+':'+str(registro.hora.minute),'%H:%M')) #registro.hora
                cont_entradas += 1
                tipo_reg_ant = 'Entrada'
            else:
                lista_entradas[cont_entradas] = datetime.strptime(str(registro.hora.hour)+':'+str(registro.hora.minute),'%H:%M') #registro.hora
                tipo_reg_ant = 'Entrada'
        else:
            #Con este if pretendo eliminar dos marcas de 'Salida' consecutivas. Se considerará la salida mas reciente y se sobreescribirá la anterior.
            if tipo_reg_ant != 'Salida':
                lista_salidas.append(datetime.strptime(str(registro.hora.hour)+':'+str(registro.hora.minute),'%H:%M')) #registro.hora
                cont_salidas += 1
                tipo_reg_ant = 'Salida'
            else:
                lista_salidas[cont_salidas] = datetime.strptime(str(registro.hora.hour)+':'+str(registro.hora.minute),'%H:%M') #registro.hora
                tipo_reg_ant = 'Salida'
    #Por el momento vamos a suponer que los empleados no hacen cualquiera y marcan de forma correcta las entradas y salidas, al menos en términos del orden 1ero entrada, luego salida.
    if cont_entradas > cont_salidas:
        #faltó marcar una salida.
        for i in range(cont_entradas):
            if i+1 == cont_entradas:
                tiempo_horas = tiempo_horas - 1
            else:
                tiempo_horas += (lista_salidas[i] - lista_entradas[i]).total_seconds() // 3600
                tiempo_mins += (lista_salidas[i] - lista_entradas[i]).total_seconds() % 3600 // 60
    #marcas completas.         
    if cont_entradas == cont_salidas:
        for i in range(cont_entradas):
            tiempo_horas += (lista_salidas[i] - lista_entradas[i]).total_seconds() // 3600
            tiempo_mins += (lista_salidas[i] - lista_entradas[i]).total_seconds() % 3600 // 60
    
    tiempo = f'{tiempo_horas:.0f}:{tiempo_mins:.0f}'
    return tiempo
            
    #El caso de que falte una entrada no puede darse porque se generarían dos marcas de salida consecutivas que se registrarían como 1 sola.