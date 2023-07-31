from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework import viewsets

from api.Serializer import ServicioSerializer,ReservasSerializer,EmpeladoSerializer,ClienteSerializer,CoordinadorSerializer
from reservas.models import Servicio,Cliente,Coordinador,Empleado, ReservaServicio


def listado_servicios(request):
    servicios = list(Servicio.objects.values())
    return JsonResponse(servicios, safe=False)


def detalle_servicio(request, id):
    servicio = Servicio.objects.get(id=id)
    servicio_dict = model_to_dict(servicio)
    return JsonResponse(servicio_dict, safe=False)

def listado_cliente(resquest):
    clientes = list(Cliente.objects.values())

    return JsonResponse(clientes, safe=False)

def lisado_coordinadores(resquest):
    coordinadores = list(Coordinador.objects.values())

    return JsonResponse(coordinadores, safe=False)

def listado_empleados(resquest):
    empelados= list(Empleado.objects.values())

    return JsonResponse(empelados, safe=False)

class ServiciosViewsSet(viewsets.ModelViewSet):
    http_method_names=('get','post','put')
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class ReservasViewsSet(viewsets.ModelViewSet):
    http_method_names=('get')
    queryset = ReservaServicio.objects.all()
    serializer_class = ReservasSerializer

class EmpleadosViewsSet(viewsets.ModelViewSet):
    http_method_names=('get','post',)
    queryset = Empleado.objects.all()
    serializer_class = EmpeladoSerializer

class ClienteViewsSet(viewsets.ModelViewSet):
    http_method_names=('get','post',)
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class CoordinadorViewsSet(viewsets.ModelViewSet):
    http_method_names=('get','post',)
    queryset = Coordinador.objects.all()
    serializer_class = CoordinadorSerializer
