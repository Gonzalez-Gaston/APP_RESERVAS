# WebApp Reservas

Esta es una aplicación web denominada WebApp Proyecto Integrador. Permite registrar los servicios ofrecidos por la empresa, así como también gestionar los empleados y clientes. Los usuarios pueden realizar reservas de servicios para los clientes y acceder a diferentes tipos de listados. Además, se puede acceder a la información de los servicios a través de un endpoint (API) que permite consultar todos los servicios disponibles y filtrarlos por su ID para ver detalles completos.

## Requisitos previos

Asegúrate de tener instalados los siguientes requisitos previos antes de comenzar:

- Django==3.2.18
- django-filter==23.2
- djangorestframework==3.14.0
- Jinja2==3.1.2

Puedes encontrarlos en el archivo `requirements.txt`. Para instalar todas las dependencias de forma rápida, utiliza el siguiente comando:

<code> pip install -r requirements.txt</code>

## Configuración inicial

Sigue estos pasos para poner en marcha la aplicación:

1. Clona este repositorio en tu máquina local.
2. Crea un entorno virtual con el siguiente comando:

<code> pip install -r requirements.txt</code>
python3 -m venv virtual


3. Activa el entorno virtual:

- En Windows:

<code> virtual\Scripts\activate</code>



- En macOS/Linux:

<code> source virtual/bin/activate</code>



4. Instala las dependencias del proyecto:


<code> pip install -r requirements.txt</code>
 


5. Crea un superusuario con el siguiente comando:

<code>python manage.py createsuperuser</code>



6. Realiza las migraciones del proyecto:

<code>python manage.py migrate</code>



7. Ejecuta el servidor:

<code>python manage.py runserver</code>



8. Accede a la aplicación en tu navegador web:


 [HOME](http://localhost:8000/home/).


## Funcionalidades del proyecto

Las funcionalidades básicas de este proyecto son las siguientes:

- Módulo de servicios: permite crear, leer, actualizar y eliminar servicios, así como mostrar un listado correspondiente. En el listado se muestran solo los servicios activos y se ofrece la posibilidad de restaurar registros no activos.

- Módulo de clientes: permite crear, leer, actualizar y eliminar clientes, así como mostrar un listado correspondiente. En el listado se muestran solo los clientes activos y se ofrece la posibilidad de restaurar registros no activos.

- Módulo de coordinadores: permite crear, leer, actualizar y eliminar coordinadores, así como mostrar un listado correspondiente. En el listado se muestran solo los coordinadores activos y se ofrece la posibilidad de restaurar registros no activos.

- Módulo de empleados: permite crear, leer, actualizar y eliminar empleados, así como mostrar un listado correspondiente. En el listado se muestran solo los empleados activos y se ofrece la posibilidad de restaurar registros no activos.

- Módulo de reservas de servicios: permite crear, leer, actualizar y eliminar reservas de servicios, así como mostrar un listado correspondiente. Se pueden crear y actualizar reservas seleccionando servicios, coordinadores, clientes y empleados activos del sistema.


## API
La api de este proyecto nos debelve los litados de clientes,empleados,cordindores,reservas de servicios en format Json. Filtra por id un servicio espesifico. 
Una vez inicializado el proyecto ouede aceder a algunos de ellos con los siguientes urls:

- [Servicios](http://localhost:8000/api/servicios/). 
- [Servicio](http://localhost:8000/api/servicios/<int:id>). 
- [Clientes](http://localhost:8000/api/clientes/).
- [Coordinadores](http://localhost:8000/api/coordinadores/).
- [Empleados](http://localhost:8000/api/empleados/). 

## admininistrador 
El administrador de Django, se  podra acceder mediante de un superusuario y contraseña creados (visto paso 5 ).Todas las clases que se observan en el archivo admin.py de la app reservas extienende de la clase admin.ModelAdmin importada de : 
- from django.contrib import admin 

En el podra ver los modelos que componen esta aplicacion web . Crear una nueva instancia de ellos y ver ciertos datos de los mismos que describiremos acontinuacion.

- Cliente: Muestra los siguiente datos del cliente en una lista :"nombre", "apellido", "activo".El listado solo apreceran los dactos activos.
        filtrar por : "nombre", "apellido". 
        ![ClienteAdmin](https://github.com/fgmc125/WebApp/blob/SC4S3-92-Tarea-Compartida-Agregar-el-archivo-Readme-al-proyecto/images/ClienteAdmin.jpg)
        

- Coordinador: Muestra los siguiente datos del cliente en una lista :'nombre', 'apellido', 'dni', 'activo', 'created', 'updated'. El listado solo apreceran los dactos activos.
           filtrar por : "nombre", "apellido".
           ![CoordinadorAdmin](https://github.com/fgmc125/WebApp/blob/SC4S3-92-Tarea-Compartida-Agregar-el-archivo-Readme-al-proyecto/images/CoordinadoresAdmin.jpg) 

- Empleado: Muestra los siguiente datos del cliente en una lista :id', 'nombre', 'apellido', 'numero_legajo', 'activo', 'created', 'updated'.El listado solo apreceran los dactos activos.
           filtrar por : "nombre", "apellido".
           ![EmpleadoAdmin](https://github.com/fgmc125/WebApp/blob/SC4S3-92-Tarea-Compartida-Agregar-el-archivo-Readme-al-proyecto/images/EmpleadoAdmin.jpg) 

- Reserva de servicio: Muestra los siguiente datos del cliente en una lista :'id', 'cliente','servicio','precio','empleado','responsable','fecha_reserva'.El listado solo apreceran los dactos activos.
           filtrar por : 'cliente__nombre','responsable__nombre''empleado__nombre','servicio__nombre'(nombre de: cliente,coordinador,e,pleado,servicio ).
           ![ReservaServicioAdmin](https://github.com/fgmc125/WebApp/blob/SC4S3-92-Tarea-Compartida-Agregar-el-archivo-Readme-al-proyecto/images/ReservasServicioAdmin.jpg)

- servicio: Muestra los siguiente datos del cliente en una lista :'nombre', 'descripcion', 'precio', 'activo'.El listado solo apreceran los dactos activos.
           filtrar por : "nombre".
           ![ServicoAdmin](https://github.com/fgmc125/WebApp/blob/SC4S3-92-Tarea-Compartida-Agregar-el-archivo-Readme-al-proyecto/images/ServicioAdmin.jpg) 

¡Disfruta utilizando WebApp Proyecto Integrador!

