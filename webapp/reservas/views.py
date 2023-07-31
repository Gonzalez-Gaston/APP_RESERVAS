import csv
import json
import os
import zipfile
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.template.loader import render_to_string
from django.views.generic import ListView

from .forms import EmpleadoForm, CoordinadorForm, ClienteForm, ServicioForm, ReservaForm
from .models import Empleado, Cliente, Coordinador, Servicio, ReservaServicio

# ------------------------------------------------------------------------------------------------
class DashBoardView(ListView):
    model = None
    context_object_name = 'test'
    queryset = []
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EmpleadoForm()
        context['services_count'] = Servicio.objects.all().count()
        context['employees_count'] = Empleado.objects.all().count()
        context['cordinators_count'] = Coordinador.objects.all().count()
        context['reservations_count'] = ReservaServicio.objects.all().count()
        context['clients_count'] = Cliente.objects.all().count()
        return context


# EMPLEADO ---------------------------------------------------------------------------------------
def list_employee_view(request, cnt=5):
    filter_mode = request.GET.get('filter', 'all')
    query = request.GET.get('search')

    if query:
        empleados = Empleado.objects.filter(nombre__icontains=query) | Empleado.objects.filter(apellido__icontains=query)
        if len(empleados) < 1:
            messages.info(request, "No se han encontrado resultados para a busqueda.")
            empleados = Servicio.objects.all()
    else:
        if 'inactive' in filter_mode:
            empleados = Empleado.objects.filter(activo=False)
        elif 'active' in filter_mode:
            empleados = Empleado.objects.filter(activo=True)
        else:
            empleados = Empleado.objects.all()

    paginator = Paginator(empleados, cnt)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'form': EmpleadoForm(),
        'empleados': items,
        'page_range': page_range,
        'cnt': cnt,
        'filter': filter_mode,
        'query': query
    }

    return render(request, 'listado_empleado.html', context)


def new_employee_view(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                employee = Empleado.objects.get(numero_legajo=form.data['numero_legajo'])
                messages.info(request, f"El numero de legajo {form.data['numero_legajo']} ya pertenece a otro empleado.")
            except Empleado.MultipleObjectsReturned:
                messages.info(request, f"El numero de legajo {form.data['numero_legajo']} ya pertenece a otro empleado.")
            except Empleado.DoesNotExist:
                form.save()
                messages.success(request, f"El empleado  fue cargado correctamente.")
        else:
            messages.error(request, f"Los datos del formulario son incorrectos")

    return HttpResponseRedirect(request.headers['Referer'])


def modificar_empleado_view(request, id):
    empleado = Empleado.objects.get(id=id)

    if request.POST:
        nombre_empleado = request.POST['nombre']
        apellido_empleado = request.POST['apellido']
        numero_legajo_empleado = request.POST['numero_legajo']

        empleado.nombre = nombre_empleado
        empleado.apellido = apellido_empleado
        empleado.numero_legajo = numero_legajo_empleado

        empleado.save()

    messages.success(request, f"El empleado {empleado.nombre} {empleado.apellido} fue modificado correctamente.")

    return HttpResponseRedirect(request.headers['Referer'])


def activate_employee_view(request, id):
    try:
        employee = get_object_or_404(Empleado, id=id)
        if not employee.activo:
            messages.success(request, f"El empleado {employee.nombre} {employee.apellido} fue activado correctamente.")
            employee.activo = True
            employee.save()
        else:
            messages.info(request, f"El empleado {employee.nombre} {employee.apellido} ya se encuentra activo.")

        return HttpResponseRedirect(request.headers['Referer'])
    except Http404:
        messages.error(request, f"No se encontro el empleado.")
        return redirect('test')  # 404 error paginaasñldmañldkña, momentaneamente Test


def desactivar_empleado(request, id):
    empleado = Empleado.objects.get(id=id)

    empleado.activo = False
    empleado.save()

    messages.success(request, f"El empleado {empleado.nombre} {empleado.apellido} fue desctivado correctamente.")

    return HttpResponseRedirect(request.headers['Referer'])

import codecs

def export_data_employee_view(request):
    # Obtener los datos que deseas exportar
    empleados = Empleado.objects.all()

    # Crear un objeto ZipFile
    zip_filename = os.path.join(settings.MEDIA_ROOT, 'export_employee.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        # Exportar datos como CSV
        csv_filename = 'empleados.csv'
        csv_path = os.path.join(settings.MEDIA_ROOT, csv_filename)
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Nombre', 'Apellido', 'Legajo', 'Imagen'])
            for empleado in empleados:
                imagen_nombre = os.path.basename(empleado.imagen.path) if empleado.imagen else ''
                writer.writerow([empleado.nombre, empleado.apellido, empleado.numero_legajo, imagen_nombre])

        # Agregar archivo CSV al ZIP
        zip_file.write(csv_path, csv_filename)

        # Exportar datos como JSON
        json_filename = 'empleados.json'
        json_path = os.path.join(settings.MEDIA_ROOT, json_filename)
        with open(json_path, 'w', encoding='utf-8') as json_file:
            data = [
                {
                    'nombre': empleado.nombre,
                    'apellido': empleado.apellido,
                    'legajo': empleado.numero_legajo,
                    'imagen': os.path.basename(empleado.imagen.path) if empleado.imagen else ''
                }
                for empleado in empleados
            ]
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        # Agregar archivo JSON al ZIP
        zip_file.write(json_path, json_filename)

        # Agregar imágenes al ZIP
        for empleado in empleados:
            if empleado.imagen:
                image_filename = os.path.basename(empleado.imagen.path)
                zip_file.write(empleado.imagen.path, image_filename)

    # Descargar el archivo ZIP
    with open(zip_filename, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="export_employee.zip"'

    # Eliminar archivos temporales
    os.remove(zip_filename)
    os.remove(csv_path)
    os.remove(json_path)

    return response

def import_data_employee_view(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']

        file_extension = os.path.splitext(file.name)[1].lower()

        if file_extension == '.csv':
            reader = csv.DictReader(file.read().decode('utf-8-sig').splitlines())
            for row in reader:
                imagen_nombre = row.get('Imagen', '')
                imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_nombre) if imagen_nombre else None
                Empleado.objects.create(
                    nombre=row['Nombre'],
                    apellido=row['Apellido'],
                    numero_legajo=row['Legajo'],
                    imagen=imagen_path
                )

        elif file_extension == '.json':
            data = json.loads(file.read().decode('utf-8'))
            for item in data:
                imagen_nombre = item.get('imagen', '')
                imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_nombre) if imagen_nombre else None
                Empleado.objects.create(
                    nombre=item['nombre'],
                    apellido=item['apellido'],
                    numero_legajo=item['legajo'],
                    #activo=item['activo'],
                    imagen=imagen_path
                )
        messages.success(request, f"Los datos se han importado correctamente.")
        return HttpResponseRedirect(request.headers['Referer'])

    messages.error(request, f"Por favor, seleccione un archivo para importar.")
    return HttpResponseRedirect(request.headers['Referer'])


# CLIENTE ----------------------------------------------------------------------------------------
def list_client_view(request, cnt=5):
    filter_mode = request.GET.get('filter', 'all')
    query = request.GET.get('search')

    if query:
        clientes = Cliente.objects.filter(nombre__icontains=query) | Cliente.objects.filter(apellido__icontains=query)
        if len(clientes) < 1:
            messages.info(request, "No se han encontrado resultados para a busqueda.")
            clientes = Servicio.objects.all()
    else:
        if 'inactive' in filter_mode:
            clientes = Cliente.objects.filter(activo=False)
        elif 'active' in filter_mode:
            clientes = Cliente.objects.filter(activo=True)
        else:
            clientes = Cliente.objects.all()

    paginator = Paginator(clientes, cnt)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'form': ClienteForm(),
        'clientes': items,
        'page_range': page_range,
        'cnt': cnt,
        'filter': filter_mode,
        'query': query
    }

    return render (request,'listado_clientes.html',context)


def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
                form.save()
                messages.success(request, f"El cliente fue cargado correctamente.")
        else:
            messages.error(request, f"Los datos del formulario son incorrectos")

    return HttpResponseRedirect(request.headers['Referer'])


def update_customer_view(request, id):
    customer = Cliente.objects.get(id=id)

    if request.POST:
        customer.nombre = request.POST['nombre']
        customer.apellido = request.POST['apellido']

        customer.save()
        messages.success(request, f"El cliente {customer.nombre} {customer.apellido} fue actualizado.")

    return HttpResponseRedirect(request.headers['Referer'])


def activar_cliente(request, id):
    cliente = Cliente.objects.get(id=id)

    cliente.activo = True
    cliente.save()

    messages.success(request, f"El empleado {cliente.nombre} {cliente.apellido} fue activado correctamente.")

    return HttpResponseRedirect(request.headers['Referer'])


def deactivate_client_view(request, id):
    try:
        client = get_object_or_404(Cliente, id=id)
        if client.activo:
            messages.success(request, f"El cliente {client.nombre} {client.apellido} fue desactivado correctamente.")
            client.activo = False
            client.save()
        else:
            messages.info(request, f"El cliente {client.nombre} {client.apellido} ya se encuentra inactivo.")

        return HttpResponseRedirect(request.headers['Referer'])
    except Http404:
        return redirect('test')

def export_data_client_view(request):
    clientes = Cliente.objects.all()

    zip_filename = os.path.join(settings.MEDIA_ROOT, 'export_client.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        csv_filename = 'clientes.csv'
        csv_path = os.path.join(settings.MEDIA_ROOT, csv_filename)
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Nombre', 'Apellido', 'Estado', 'Imagen'])
            for cliente in clientes:
                imagen_nombre = os.path.basename(cliente.imagen.path) if cliente.imagen else ''
                writer.writerow([cliente.nombre, cliente.apellido, cliente.activo, imagen_nombre])

        zip_file.write(csv_path, csv_filename)

        json_filename = 'clientes.json'
        json_path = os.path.join(settings.MEDIA_ROOT, json_filename)
        with open(json_path, 'w', encoding='utf-8') as json_file:
            data = [
                {
                    'nombre': cliente.nombre,
                    'apellido': cliente.apellido,
                    'activo': cliente.activo,
                    'imagen': os.path.basename(cliente.imagen.path) if cliente.imagen else ''
                }
                for cliente in clientes
            ]
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        zip_file.write(json_path, json_filename)

        for cliente in clientes:
            if cliente.imagen:
                image_filename = os.path.basename(cliente.imagen.path)
                zip_file.write(cliente.imagen.path, image_filename)

    with open(zip_filename, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="export_client.zip"'

    # Eliminar archivos temporales
    os.remove(zip_filename)
    os.remove(csv_path)
    os.remove(json_path)

    return response


def import_data_client_view(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']

        file_extension = os.path.splitext(file.name)[1].lower()

        if file_extension == '.csv':
            reader = csv.DictReader(file.read().decode('utf-8-sig').splitlines())
            for row in reader:
                imagen_nombre = row.get('Imagen', '')
                imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_nombre) if imagen_nombre else None
                Cliente.objects.create(
                    nombre=row['Nombre'],
                    apellido=row['Apellido'],
                    activo=row['Estado'],
                    imagen=imagen_path
                )

        elif file_extension == '.json':
            data = json.loads(file.read().decode('utf-8'))
            for item in data:
                imagen_nombre = item.get('imagen', '')
                imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_nombre) if imagen_nombre else None
                Cliente.objects.create(
                    nombre=item['nombre'],
                    apellido=item['apellido'],
                    activo=item['estado'],
                    imagen=imagen_path
                )
        messages.success(request, f"Los datos se han importado correctamente.")
        return HttpResponseRedirect(request.headers['Referer'])

    messages.error(request, f"Por favor, seleccione un archivo para importar.")
    return HttpResponseRedirect(request.headers['Referer'])


# COORDINADOR ------------------------------------------------------------------------------------
def list_coordinator_view(request, cnt=5):
    filter_mode = request.GET.get('filter', 'all')
    query = request.GET.get('search')

    if query:
        coordinadores = Coordinador.objects.filter(nombre__icontains=query) | Coordinador.objects.filter(apellido__icontains=query)
        if len(coordinadores) < 1:
            messages.info(request, "No se han encontrado resultados para a busqueda.")
            coordinadores = Servicio.objects.all()
    else:
        if 'inactive' in filter_mode:
            coordinadores = Coordinador.objects.filter(activo=False)
        elif 'active' in filter_mode:
            coordinadores = Coordinador.objects.filter(activo=True)
        else:
            coordinadores = Coordinador.objects.all()

    paginator = Paginator(coordinadores, cnt)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'form': CoordinadorForm(),
        'coordinadores': items,
        'page_range': page_range,
        'cnt': cnt,
        'filter': filter_mode,
        'query': query
    }

    return render(request, 'listado_coordinadores.html', context)


def nuevo_coordinador(request):
    if request.method == 'POST':
        form = CoordinadorForm(request.POST, request.FILES)
        if form.is_valid():
                form.save()
                messages.success(request, f"El coordinador fue cargado correctamente.")
        else:
            messages.error(request, f"Los datos del formulario son incorrectos")

    return HttpResponseRedirect(request.headers['Referer'])


def update_coordinators_view(request, id):
    coordinators = Coordinador.objects.get(id=id)

    if request.POST:
        coordinators.nombre = request.POST['nombre']
        coordinators.apellido = request.POST['apellido']
        coordinators.dni = request.POST['dni']
        
        coordinators.save()
        messages.success(request, f"El coordinador {coordinators.nombre} {coordinators.apellido} fue actualizado.")

    return HttpResponseRedirect(request.headers['Referer'])


def activar_coordiandor(request, id):
    coordinador = Coordinador.objects.get(id=id)

    coordinador.activo = True
    coordinador.save()

    messages.success(request, f"El coordinador {coordinador.nombre} {coordinador.apellido} fue activado correctamente.")
    return HttpResponseRedirect(request.headers['Referer'])


def deactivate_coordinator_view(request, id):
    try:
        coordinator = get_object_or_404(Coordinador, id=id)
        if coordinator.activo:
            messages.success(request, f"El cordinador {coordinator.nombre} {coordinator.apellido} fue desactivado correctamente.")
            coordinator.activo = False
            coordinator.save()
        else:
            messages.info(request, f"El coordinador {coordinator.nombre} {coordinator.apellido} ya se encuentra inactivo.")

        # No hay lista de Coordinadores todavia, luego se modifica
        return HttpResponseRedirect(request.headers['Referer'])
    except Http404:
        # 404 error paginaasñldmañldkña, momentaneamente Test
        return redirect('test')


def export_data_coordinator_view(request):
    coordinadores = Coordinador.objects.all()

    zip_filename = os.path.join(settings.MEDIA_ROOT, 'export_coordinator.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        csv_filename = 'coordinadores.csv'
        csv_path = os.path.join(settings.MEDIA_ROOT, csv_filename)
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Nombre', 'Apellido', 'DNI', 'Estado', 'Imagen'])
            for coordinador in coordinadores:
                imagen_nombre = os.path.basename(coordinador.imagen.path) if coordinador.imagen else ''
                writer.writerow([coordinador.nombre, coordinador.apellido, coordinador.dni, coordinador.activo, imagen_nombre])

        zip_file.write(csv_path, csv_filename)

        json_filename = 'coordinadores.json'
        json_path = os.path.join(settings.MEDIA_ROOT, json_filename)
        with open(json_path, 'w', encoding='utf-8') as json_file:
            data = [
                {
                    'nombre': coordinador.nombre,
                    'apellido': coordinador.apellido,
                    'dni': coordinador.dni,
                    'estado': coordinador.activo,
                    'imagen': os.path.basename(coordinador.imagen.path) if coordinador.imagen else ''
                }
                for coordinador in coordinadores
            ]
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        zip_file.write(json_path, json_filename)

        for coordinador in coordinadores:
            if coordinador.imagen:
                image_filename = os.path.basename(coordinador.imagen.path)
                zip_file.write(coordinador.imagen.path, image_filename)

    with open(zip_filename, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="export_coordinator.zip"'

    # Eliminar archivos temporales
    os.remove(zip_filename)
    os.remove(csv_path)
    os.remove(json_path)

    return response


def import_data_coordinator_view(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']

        file_extension = os.path.splitext(file.name)[1].lower()

        if file_extension == '.csv':
            reader = csv.DictReader(file.read().decode('utf-8-sig').splitlines())
            for row in reader:
                imagen_nombre = row.get('Imagen', '')
                imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_nombre) if imagen_nombre else None
                Coordinador.objects.create(
                    nombre=row['Nombre'],
                    apellido=row['Apellido'],
                    dni=row['DNI'],
                    activo=row['Estado'],
                    imagen=imagen_path
                )

        elif file_extension == '.json':
            data = json.loads(file.read().decode('utf-8'))
            for item in data:
                imagen_nombre = item.get('imagen', '')
                imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_nombre) if imagen_nombre else None
                Coordinador.objects.create(
                    nombre=item['nombre'],
                    apellido=item['apellido'],
                    dni=item['dni'],
                    activo=item['Estado'],
                    imagen=imagen_path
                )
        messages.success(request, f"Los datos se han importado correctamente.")
        return HttpResponseRedirect(request.headers['Referer'])

    messages.error(request, f"Por favor, seleccione un archivo para importar.")
    return HttpResponseRedirect(request.headers['Referer'])

# SERVICIO ---------------------------------------------------------------------------------------
def list_service_view(request, cnt=5):
    filter_mode = request.GET.get('filter', 'all')
    query = request.GET.get('search')

    if query:
        servicios = Servicio.objects.filter(nombre__icontains=query)
        if len(servicios) < 1:
            messages.info(request, "No se han encontrado resultados para a busqueda.")
            servicios = Servicio.objects.all()
    else:
        if 'inactive' in filter_mode:
            servicios = Servicio.objects.filter(activo=False)
        elif 'active' in filter_mode:
            servicios = Servicio.objects.filter(activo=True)
        else:
            servicios = Servicio.objects.all()

    paginator = Paginator(servicios, cnt)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]


    context = {
        'form': ServicioForm(),
        'titulo_singular': "servicio",
        'titulo_plural': "servicios",
        'headers': ["ID", "Nombre", "Precio", "Activo"],
        'servicios': items,
        'page_range': page_range,
        'cnt': cnt,
        'filter': filter_mode,
        'query': query
    }

    return render(request, 'listado_servicios.html', context)


def new_service_view(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"La servicio fue cargada correctamente.")
        else:
            messages.error(request, f"Los datos del formulario son incorrectos")

    return HttpResponseRedirect(request.headers['Referer'])


def update_service_view(request, id):
    if request.method == 'POST':
        servicio = Servicio.objects.get(id=id)
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, f"La servicio fue cargada correctamente.")
        else:
            messages.error(request, f"Los datos del formulario son incorrectos")

    return HttpResponseRedirect(request.headers['Referer'])


def activar_servicio(request, id):
    servicio = Servicio.objects.get(id=id)

    servicio.activo = True
    servicio.save()

    messages.success(request, f"El servicio {servicio.nombre} fue activado correctamente!")

    return HttpResponseRedirect(request.headers['Referer'])


def deactivate_service_view(request, id):
    try:
        service = get_object_or_404(Servicio, id=id)
        if service.activo:
            messages.success(request, f"El servicio {service.nombre} fue desactivado correctamente.")
            service.activo = False
            service.save()
        else:
            messages.info(request, f"El servicio {service.nombre} a se encuentra inactivo.")

        return HttpResponseRedirect(request.headers['Referer'])
    except Http404:
        # 404 error paginaasñldmañldkña, momentaneamente Home
        return redirect('home')


def export_data_service_view(request):
    servicios = Servicio.objects.all()

    zip_filename = os.path.join(settings.MEDIA_ROOT, 'export_service.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        csv_filename = 'servicios.csv'
        csv_path = os.path.join(settings.MEDIA_ROOT, csv_filename)
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Nombre', 'Descripcion', 'Precio', 'Estado', 'Imagen'])
            for servicio in servicios:
                imagen_nombre = os.path.basename(servicio.imagen.path) if servicio.imagen else ''
                writer.writerow([servicio.nombre, servicio.descripcion, servicio.precio, servicio.activo, imagen_nombre])

        zip_file.write(csv_path, csv_filename)

        json_filename = 'servicios.json'
        json_path = os.path.join(settings.MEDIA_ROOT, json_filename)
        with open(json_path, 'w', encoding='utf-8') as json_file:
            data = [
                {
                    'nombre': servicio.nombre,
                    'descripcion': servicio.descripcion,
                    'precio': servicio.precio,
                    'estado': servicio.activo,
                    'imagen': os.path.basename(servicio.imagen.path) if servicio.imagen else ''
                }
                for servicio in servicios
            ]
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        zip_file.write(json_path, json_filename)

        for servicio in servicios:
            if servicio.imagen:
                image_filename = os.path.basename(servicio.imagen.path)
                zip_file.write(servicio.imagen.path, image_filename)

    with open(zip_filename, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="export_service.zip"'

    # Eliminar archivos temporales
    os.remove(zip_filename)
    os.remove(csv_path)
    os.remove(json_path)

    return response


def import_data_service_view(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']

        file_extension = os.path.splitext(file.name)[1].lower()

        if file_extension == '.csv':
            reader = csv.DictReader(file.read().decode('utf-8-sig').splitlines())
            for row in reader:
                imagen_nombre = row.get('Imagen', '')
                imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_nombre) if imagen_nombre else None
                Servicio.objects.create(
                    nombre=row['Nombre'],
                    descripcion=row['Descripcion'],
                    precio=row['Precio'],
                    activo=row['Estado'],
                    imagen=imagen_path
                )

        elif file_extension == '.json':
            data = json.loads(file.read().decode('utf-8'))
            for item in data:
                imagen_nombre = item.get('imagen', '')
                imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_nombre) if imagen_nombre else None
                Servicio.objects.create(
                    nombre=item['nombre'],
                    descripcion=item['descripcion'],
                    precio=item['precio'],
                    activo=item['Estado'],
                    imagen=imagen_path
                )
        messages.success(request, f"Los datos se han importado correctamente.")
        return HttpResponseRedirect(request.headers['Referer'])

    messages.error(request, f"Por favor, seleccione un archivo para importar.")
    return HttpResponseRedirect(request.headers['Referer'])

# RESERVA ----------------------------------------------------------------------------------------
def list_reserve_view(request, cnt=5):
    filter_mode = request.GET.get('filter', 'all')
    query = request.GET.get('search')

    if query:
        reservas = ReservaServicio.objects.filter(nombre__icontains=query) | ReservaServicio.objects.filter(apellido__icontains=query)
    else:
        if 'inactive' in filter_mode:
            reservas = ReservaServicio.objects.filter(activo=False)
        elif 'active' in filter_mode:
            reservas = ReservaServicio.objects.filter(activo=True)
        else:
            reservas = ReservaServicio.objects.all()

    paginator = Paginator(reservas, cnt)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    lista_servicio = Servicio.objects.filter(activo=True)
    lista_empleados = Empleado.objects.filter(activo=True)
    lista_clientes = Cliente.objects.filter(activo=True)
    lista_coordinadores = Coordinador.objects.filter(activo=True)

    context = {
        'form': ReservaForm(),
        'reservas': items,
        'page_range': page_range,
        'cnt': cnt,
        'filter': filter_mode,
        'query': query,
        "servicios": lista_servicio,
        "empleados": lista_empleados,
        "clientes": lista_clientes,
        "coordinadores": lista_coordinadores,
        'titulo_singular': "Reserva",
        'titulo_plural': "Reservas",
        'headers': ["Fecha de Reserva",
                    "Cliente",
                    "Responsable",
                    "Empleado",
                    "Servicio",
                    "Precio"],
    }

    return render(request, 'listado_reservas.html', context)


def new_reservation_view(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, f"La reserva fue cargada correctamente.")
            else:
                messages.error(request, f"Los datos del formulario son incorrectos")
        except ValidationError as e:
            messages.error(request, str(e))

    return HttpResponseRedirect(request.headers['Referer'])


def update_reserva(request, id):
    if request.method == 'POST':
        #reserva = ReservaServicio.objects.get(id=id)
        reserva = get_object_or_404(ReservaServicio, id=id)
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, f"La reserva fue actualizada correctamente.")
        else:
            messages.error(request, f"Los datos del formulario son incorrectos")

    return HttpResponseRedirect(request.headers['Referer'])

def eliminar_reserva(request, id):
    reserva = ReservaServicio.objects.get(id=id)
    reserva.delete()
    messages.success(request, f"La reserva fue eliminada correctamente!")
    return HttpResponseRedirect(request.headers['Referer'])


def export_data_reserve_view(request):
    servicios = Servicio.objects.all()

    zip_filename = os.path.join(settings.MEDIA_ROOT, 'export_service.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        csv_filename = 'servicios.csv'
        csv_path = os.path.join(settings.MEDIA_ROOT, csv_filename)
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Nombre', 'Descripcion', 'Precio', 'Estado', 'Imagen'])
            for servicio in servicios:
                imagen_nombre = os.path.basename(servicio.imagen.path) if servicio.imagen else ''
                writer.writerow([servicio.nombre, servicio.descripcion, servicio.precio, servicio.activo, imagen_nombre])

        zip_file.write(csv_path, csv_filename)

        json_filename = 'servicios.json'
        json_path = os.path.join(settings.MEDIA_ROOT, json_filename)
        with open(json_path, 'w', encoding='utf-8') as json_file:
            data = [
                {
                    'nombre': servicio.nombre,
                    'descripcion': servicio.descripcion,
                    'precio': servicio.precio,
                    'estado': servicio.activo,
                    'imagen': os.path.basename(servicio.imagen.path) if servicio.imagen else ''
                }
                for servicio in servicios
            ]
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        zip_file.write(json_path, json_filename)

        for servicio in servicios:
            if servicio.imagen:
                image_filename = os.path.basename(servicio.imagen.path)
                zip_file.write(servicio.imagen.path, image_filename)

    with open(zip_filename, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="export_service.zip"'

    # Eliminar archivos temporales
    os.remove(zip_filename)
    os.remove(csv_path)
    os.remove(json_path)

    return response


def import_data_reserve_view(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']

        file_extension = os.path.splitext(file.name)[1].lower()

        if file_extension == '.csv':
            reader = csv.DictReader(file.read().decode('utf-8-sig').splitlines())
            for row in reader:
                imagen_nombre = row.get('Imagen', '')
                imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_nombre) if imagen_nombre else None
                Coordinador.objects.create(
                    nombre=row['Nombre'],
                    descripcion=row['Descripcion'],
                    precio=row['Precio'],
                    activo=row['Estado'],
                    imagen=imagen_path
                )

        elif file_extension == '.json':
            data = json.loads(file.read().decode('utf-8'))
            for item in data:
                imagen_nombre = item.get('imagen', '')
                imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_nombre) if imagen_nombre else None
                Cliente.objects.create(
                    nombre=item['nombre'],
                    descripcion=item['descripcion'],
                    precio=item['precio'],
                    activo=item['Estado'],
                    imagen=imagen_path
                )
        messages.success(request, f"Los datos se han importado correctamente.")
        return HttpResponseRedirect(request.headers['Referer'])

    messages.error(request, f"Por favor, seleccione un archivo para importar.")
    return HttpResponseRedirect(request.headers['Referer'])
# TOOLS ------------------------------------------------------------------------------------------

def import_data_service_view_full(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']

        file_extension = os.path.splitext(file.name)[1].lower()

        if file_extension == '.zip':
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_contents = zip_ref.namelist()

                if 'servicios.csv' in zip_contents:
                    with zip_ref.open('servicios.csv') as csv_file:
                        reader = csv.DictReader(csv_file.read().decode('utf-8-sig').splitlines())
                        for row in reader:
                            imagen_nombre = row.get('Imagen', '')
                            imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_nombre) if imagen_nombre else None
                            Servicio.objects.create(
                                nombre=row['Nombre'],
                                descripcion=row['Descripcion'],
                                precio=row['Precio'],
                                activo=row['Estado'],
                                imagen=imagen_path
                            )

                for image_filename in zip_contents:
                    if image_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                        image_path = os.path.join(settings.MEDIA_ROOT, image_filename)
                        with open(image_path, 'wb') as image_file:
                            image_file.write(zip_ref.read(image_filename))

        elif file_extension == '.csv':
            reader = csv.DictReader(file.read().decode('utf-8-sig').splitlines())
            for row in reader:
                imagen_nombre = row.get('Imagen', '')
                imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_nombre) if imagen_nombre else None
                Servicio.objects.create(
                    nombre=row['Nombre'],
                    descripcion=row['Descripcion'],
                    precio=row['Precio'],
                    activo=row['Estado'],
                    imagen=imagen_path
                )

        elif file_extension == '.json':
            data = json.loads(file.read().decode('utf-8'))
            for item in data:
                imagen_nombre = item.get('imagen', '')
                imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_nombre) if imagen_nombre else None
                Servicio.objects.create(
                    nombre=item['nombre'],
                    descripcion=item['descripcion'],
                    precio=item['precio'],
                    activo=item['Estado'],
                    imagen=imagen_path
                )

        messages.success(request, "Los datos se han importado correctamente.")
        return HttpResponseRedirect(request.headers.get('Referer', '/'))

    messages.error(request, "Por favor, seleccione un archivo para importar.")
    return HttpResponseRedirect(request.headers.get('Referer', '/'))