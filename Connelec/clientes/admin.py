from django.contrib import admin
from .models import Cliente
# Register your models here.
class CLienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cuit', 'telefono', 'email', 'fecha_creacion']
    list_filter = ['nombre', 'cuit', 'telefono', 'email']
    search_fields = ['nombre', 'cuit', 'telefono', 'email']
    list_per_page = 30
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
admin.site.register(Cliente)