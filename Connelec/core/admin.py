from django.contrib import admin


# # Register your models here.
# class TareasAdmin(admin.ModelAdmin):
#     list_display = ['nombre', 'descrip', 'encargado', 'estado', 'fecha_entrega', 'fecha_creacion', 'fecha_actualizacion']
#     list_filter = ['encargado','estado', 'fecha_entrega', 'fecha_creacion', 'fecha_actualizacion']
#     search_fields = ['nombre', 'descrip', 'encargado']
#     list_per_page = 30
#     readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
# admin.site.register(Tareas, TareasAdmin)

# class ArchivosAdmin(admin.ModelAdmin):
#     list_display = ['nombre', 'tarea', 'archivo', 'fecha_creacion', 'fecha_actualizacion']
#     list_filter = ['tarea', 'fecha_creacion', 'fecha_actualizacion']
#     search_fields = ['nombre', 'tarea']
#     list_per_page = 30
#     readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
# admin.site.register(Archivos)

# class Entrada_historialAdmin(admin.ModelAdmin):
#     list_display = ['fecha_actualizacion', 'resumen', 'tarea', 'adjunto', 'fecha_creacion']
#     list_filter = ['tarea', 'fecha_creacion']
#     search_fields = ['tarea']
#     list_per_page = 30
#     readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
# admin.site.register(Entrada_historial)

