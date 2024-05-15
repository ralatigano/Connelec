from django.contrib import admin
from .models import Proyectos
# Register your models here.
class ProyectosAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cliente', 'fecha_creacion', 'fecha_actualizacion']
    list_filter = ['nombre','cliente', 'fecha_creacion', 'fecha_actualizacion']
    search_fields = ['nombre','cliente']
    list_per_page = 30
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
admin.site.register(Proyectos, ProyectosAdmin)