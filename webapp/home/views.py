from django.shortcuts import render
from django.views.generic import ListView


# Create your views here.
class HomeView(ListView):
    model = None
    context_object_name = 'test'
    queryset = []
    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = EmpleadoForm()
        # context['services_count'] = Servicio.objects.all().count()
        # context['employees_count'] = Empleado.objects.all().count()
        # context['cordinators_count'] = Coordinador.objects.all().count()
        # context['reservations_count'] = ReservaServicio.objects.all().count()
        # context['clients_count'] = Cliente.objects.all().count()
        return context

class ContactoView(ListView):
    model = None
    context_object_name = 'test'
    queryset = []
    template_name = 'contacto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = EmpleadoForm()
        # context['services_count'] = Servicio.objects.all().count()
        # context['employees_count'] = Empleado.objects.all().count()
        # context['cordinators_count'] = Coordinador.objects.all().count()
        # context['reservations_count'] = ReservaServicio.objects.all().count()
        # context['clients_count'] = Cliente.objects.all().count()
        return context


class NosotrosView(ListView):
    model = None
    context_object_name = 'test'
    queryset = []
    template_name = 'nosotros.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = EmpleadoForm()
        # context['services_count'] = Servicio.objects.all().count()
        # context['employees_count'] = Empleado.objects.all().count()
        # context['cordinators_count'] = Coordinador.objects.all().count()
        # context['reservations_count'] = ReservaServicio.objects.all().count()
        # context['clients_count'] = Cliente.objects.all().count()
        return context


class FotosView(ListView):
    model = None
    context_object_name = 'test'
    queryset = []
    template_name = 'fotos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = EmpleadoForm()
        # context['services_count'] = Servicio.objects.all().count()
        # context['employees_count'] = Empleado.objects.all().count()
        # context['cordinators_count'] = Coordinador.objects.all().count()
        # context['reservations_count'] = ReservaServicio.objects.all().count()
        # context['clients_count'] = Cliente.objects.all().count()
        return context