from django.contrib import admin
from .models import registro, User, Reporte

# Register your models here.
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_completo', 'usuario', 'fecha', 'hora', 'tipo')


admin.site.register(registro, RegistroAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.register(User, UserAdmin)

class ReporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'hora', 'informe')

admin.site.register(Reporte, ReporteAdmin)

