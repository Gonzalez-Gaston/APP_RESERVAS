from rest_framework import  serializers
from reservas.views import Servicio,ReservaServicio,Empleado,Cliente,Coordinador

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ('id', 'nombre', 'descripcion','precio')

class ReservasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaServicio
        fields = ('id', 'fecha_reserva', 'cliente','responsable','empleado','servicio', 'precio')
        depth = 1 


class EmpeladoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ('id', 'nombre','apellido','numero_legajo' )

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'nombre','apellido')


class CoordinadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinador
        fields = ('id', 'nombre','apellido','dni')