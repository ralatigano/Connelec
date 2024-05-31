from django.contrib import admin
# cambio esto para probar un modelo de usuario con una relación OneToOneField con User
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import registro, Reporte_tarea, Usuario  # User,
from django.contrib.auth.models import User


# Register your models here.
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_completo',
                    'usuario', 'fecha', 'hora', 'tipo')


admin.site.register(registro, RegistroAdmin)

# cambio esto para probar un modelo de usuario con una aplicación OneToOneField con User
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton


class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = "usuarios"

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = [UsuarioInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email',
#                     'first_name', 'last_name', 'is_staff')

# admin.site.register(UserAdmin)


class ReporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'hora', 'informe')
    list_filter = ('usuario', 'fecha', 'proyecto')


admin.site.register(Reporte_tarea, ReporteAdmin)
