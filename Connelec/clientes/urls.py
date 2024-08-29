from django.urls import path
from .views import (
    clientes, ver_clientes, nuevo_cliente, editar_cliente, borrar_cliente
)

urlpatterns = [
    # Menu clientes
    path('', clientes, name='clientes'),
    # CRUD clientes
    path('verClientes', ver_clientes, name='ver_clientes'),
    path('nuevoCliente', nuevo_cliente, name='nuevo_cliente'),
    path('editarCliente', editar_cliente, name='editar_cliente'),
    path('borrarCliente/<int:id>', borrar_cliente, name='borrar_cliente')
]
