from django.db import models


class Empleado(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=150, verbose_name="Apellido")
    numero_legajo = models.PositiveIntegerField(verbose_name="Numero de legajo", help_text='')
    activo = models.BooleanField(default=True, verbose_name="¿Está activo?")
    imagen = models.ImageField(upload_to='upload/img/empleados/', null=True, blank=True, verbose_name='Imagen')

    created = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Actualizado el", auto_now=True)

    class Meta:
        db_table = 'empleado_db'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return self.nombre


class Coordinador(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=150, verbose_name="Apellido")
    dni = models.PositiveIntegerField(verbose_name="DNI", help_text='')
    activo = models.BooleanField(default=True, verbose_name="¿Está activo?")
    imagen = models.ImageField(upload_to='upload/img/coordinador/', null=True, blank=True, verbose_name='Imagen')

    created = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Actualizado el", auto_now=True)

    class Meta:
        db_table = 'coordinador_db'
        verbose_name = 'Coordinador'
        verbose_name_plural = 'Coordinadores'

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=40, blank=False, null=False, verbose_name="Nombre")
    apellido = models.CharField(max_length=40, blank=False, null=False, verbose_name="Apellido")
    activo = models.BooleanField(default=True, blank=False, null=False, verbose_name="Activo")
    imagen = models.ImageField(upload_to='upload/img/clientes/', null=True, blank=True, verbose_name='Imagen')

    created = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Actualizado el", auto_now=True)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.CharField(max_length=150, verbose_name="Descripcion")
    precio = models.IntegerField(verbose_name="Precio", help_text='')
    activo = models.BooleanField(default=True, verbose_name="¿Está activo?")
    imagen = models.ImageField(upload_to='upload/img/servicios/', null=True, blank=True, verbose_name='Imagen')

    created = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Actualizado el", auto_now=True)

    class Meta:
        db_table = 'Servicio_db'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.nombre


class ReservaServicio(models.Model):
    created = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Actualizado el", auto_now=True)
    fecha_reserva = models.DateTimeField(verbose_name="Reserva para el")

    cliente = models.ForeignKey(Cliente, related_name="reservas", on_delete=models.CASCADE)
    responsable = models.ForeignKey(Coordinador, related_name="reservas", on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, related_name="reservas", on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, related_name="reservas", on_delete=models.CASCADE)
    precio = models.IntegerField(verbose_name="precio", default=0)

    class Meta:
        db_table = 'Reserva_Servicio_db'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
