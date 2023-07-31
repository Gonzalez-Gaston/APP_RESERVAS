from django.contrib import admin
from .models import Empleado,Cliente,Coordinador,Servicio,ReservaServicio


class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'apellido', 'numero_legajo', 'activo', 'created', 'updated']
    search_fields = ['nombre', 'apellido']
    list_filter = ['activo']
    readonly_fields = ('id', 'created', 'updated')


admin.site.register(Empleado, EmpleadoAdmin)

class ClienteAdmin(admin.ModelAdmin):
    list_display = ["nombre", "apellido", "activo"]
    search_fields = ["nombre", "apellido"]
    list_filter = ['activo']
    readonly_fields = ('id', 'created', 'updated')

admin.site.register(Cliente, ClienteAdmin)


class CoordinadorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'dni', 'activo', 'created', 'updated']
    search_fields = ['nombre', 'apellido']
    list_filter = ['activo']
    readonly_fields = ('created', 'updated')


admin.site.register(Coordinador, CoordinadorAdmin)


class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'precio', 'activo']
    search_fields = ['nombre']
    list_filter = ['activo']
    readonly_fields = ('id', 'created', 'updated')

admin.site.register(Servicio, ServicioAdmin)

class ReservaServicioAdmin(admin.ModelAdmin):
    model = ReservaServicio
    list_display = ['id', 'cliente','servicio','precio','empleado','responsable','fecha_reserva']
    search_fields = [
        'cliente__nombre',
        'responsable__nombre',
        'empleado__nombre',
        'servicio__nombre',
    ]
    readonly_fields = ('id',)

admin.site.register(ReservaServicio, ReservaServicioAdmin)