import uuid

from django import forms
from django.core.files.storage import default_storage

from reservas.models import Empleado, Cliente, Coordinador, Servicio, ReservaServicio
from PIL import Image

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'numero_legajo','imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el Nombre'})
        self.fields['apellido'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el Apellido'})
        self.fields['numero_legajo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el Número de legajo'})
        self.fields['imagen'].widget.attrs.update({'class': 'form-control'})

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido','imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el Nombre'})
        self.fields['apellido'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el Apellido'})
        self.fields['imagen'].widget.attrs.update({'class': 'form-control'})

class CoordinadorForm(forms.ModelForm):
    class Meta:
        model = Coordinador
        fields = ['nombre', 'apellido', 'dni','imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el Nombre'})
        self.fields['apellido'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el Apellido'})
        self.fields['dni'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el Número de DNI '})
        self.fields['imagen'].widget.attrs.update({'class': 'form-control'})

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio', 'imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el Nombre'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese una descipción'})
        self.fields['precio'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el precio'})
        self.fields['imagen'].widget.attrs.update({'class': 'form-control'})


class ReservaForm(forms.ModelForm):
    class Meta:
        model = ReservaServicio
        fields = ['cliente','servicio','empleado','responsable','precio', 'fecha_reserva']
        widgets = {
            'fecha_reserva': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].widget.attrs.update({'class': 'form-control'})
        self.fields['servicio'].widget.attrs.update({'class': 'form-control'})
        self.fields['precio'].widget.attrs.update({'class': 'form-control'})
        self.fields['responsable'].widget.attrs.update({'class': 'form-control'})
        self.fields['empleado'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_reserva'].widget.attrs.update({'class': 'form-control'})
