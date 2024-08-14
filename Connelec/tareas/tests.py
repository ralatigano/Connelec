from tareas.models import Entrada_historial


def Manejo_entradas():
    entradas = Entrada_historial.objects.filter(proyecto=1)
    dict_fechas = {}
    for e in entradas:
        fecha_formateada = e.fecha.strftime("%d/%m/%Y")
        dict_fechas[e.id] = fecha_formateada
    list_llaves = list(dict_fechas.keys())
    print(list_llaves)
