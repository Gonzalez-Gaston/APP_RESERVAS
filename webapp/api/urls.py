from django.urls import path, include
from rest_framework import routers


from api.views import ServiciosViewsSet,CoordinadorViewsSet,EmpleadosViewsSet,ClienteViewsSet,ReservasViewsSet
from .views import (
    detalle_servicio,
    listado_cliente,
    lisado_coordinadores,
    listado_empleados,
    listado_servicios,
    )

router = routers.DefaultRouter()
router.register(r'servicios', ServiciosViewsSet, basename='servicios')
router.register(r'coordinador', CoordinadorViewsSet, basename='cordinador')
router.register(r'empleado', EmpleadosViewsSet, basename='empleado')
router.register(r'cliente', ClienteViewsSet, basename='cliente')
router.register(r'reserva', ReservasViewsSet, basename='reserva')

urlpatterns = [
    path('api/servicios/', listado_servicios, name='servicios'),
    path('api/v2',include(router.urls)),
    path('api/v2/',include(router.urls)),
    path('api/servicios/<int:id>', detalle_servicio, name='servicio'),
    #-------------------Clientes----------------------
    path('api/clientes/', listado_cliente,name='clientes' ),
    #-------------------Cordinadores-------------------
    path('api/coordinadores/', lisado_coordinadores, name='coordinadores'),
    #-------------------Empleados------------------------
    path('api/empleados/',listado_empleados,name='empleados')
]