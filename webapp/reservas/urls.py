from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from reservas import views


urlpatterns = [
    # BASIC VIEW -------------------------------------------------------------------------------------------------
    path('dashboard/', views.DashBoardView.as_view(), name='dashboard'),
    path('dashboard', views.DashBoardView.as_view(), name='dashboard'),
    # EMPLEADOS --------------------------------------------------------------------------------------------------
    path('empleados/listado/', views.list_employee_view, name='list_employee'),
    path('empleados/listado/<int:cnt>/', views.list_employee_view, name='list_employee_cnt'),
    path('empleados/nuevo', views.new_employee_view, name='new-employee'),
    path('empleados/modificar/<int:id>', views.modificar_empleado_view, name='modificar'),
    path('empleados/activar/<int:id>', views.activate_employee_view, name='activate-employee'),
    path('empleados/desactivar/<int:id>', views.desactivar_empleado, name='desactivar_empleado'),
    # COORDINATORS ------------------------------------------------------------------------------------------------
    path('coordinadores/listado/',views.list_coordinator_view, name='list_coordinator'),
    path('coordinadores/listado/<int:cnt>/', views.list_coordinator_view, name='list_coordinator'),
    path('coordinadores/nuevo', views.nuevo_coordinador, name='nuevo_coordinador'),
    path('coordinadored/modificar/<int:id>', views.update_coordinators_view, name='modificar_cordinador'),
    path('coordinadores/activar/<int:id>', views.activar_coordiandor, name='activar_coordinador'),
    path('coordinadores/desactivar/<int:id>', views.deactivate_coordinator_view, name='deactivate-coordinator'),
    # CLIENTS -----------------------------------------------------------------------------------------------------
    path('clientes/listado/', views.list_client_view, name='lista_cliente'),
    path('clientes/listado/<int:cnt>/', views.list_client_view, name='lista_cliente'),
    path('clientes/nuevo', views.nuevo_cliente, name='nuevo_cliente'),
    path('clientes/modificar/<int:id>', views.update_customer_view, name='modificar-client'),
    path('clientes/activar/<int:id>', views.activar_cliente, name='activar_cliente'),
    path('clientes/desactivar/<int:id>', views.deactivate_client_view, name='deactivate-client'),
    # SERVICES ----------------------------------------------------------------------------------------------------
    path('servicios/listado/', views.list_service_view, name='services_list'),
    path('servicios/listado/<int:cnt>/', views.list_service_view, name='services_list'),
    path('servicios/nuevo', views.new_service_view, name='new-service'),
    path('servicios/modificar/<int:id>', views.update_service_view, name='update-service'),
    path('servicios/activar/<int:id>', views.activar_servicio, name='activar_servicio'),
    path('servicios/desactivar/<int:id>', views.deactivate_service_view, name='deactivate-service'),
    # RESERVA -----------------------------------------------------------------------------------------------------
    path('reservas/listado/', views.list_reserve_view, name='reservations-list'),
    path('reservas/listado/<int:cnt>/', views.list_reserve_view, name='reservations-list'),
    path('reservas/nuevo', views.new_reservation_view, name='new-reservation'),
    path('reservas/modificar/<int:id>', views.update_reserva, name='modificar-reserva'),
    path('reservas/eliminar/<int:id>', views.eliminar_reserva, name='eliminar_reserva'),
    # TESTING -----------------------------------------------------------------------------------------------------
    # path('empleados/export/<str:format>/', views.export_data_view, name='export_data_csv_json'),
    path('empleados/export/', views.export_data_employee_view, name='export_data_employee'),
    path('empleados/import/', views.import_data_employee_view, name='import_data_employee'),

    path('clientes/export/', views.export_data_client_view, name='export_data_client'),
    path('clientes/import/', views.import_data_client_view, name='import_data_client'),

    path('coordinadores/export/', views.export_data_coordinator_view, name='export_data_coordinator'),
    path('coordinadores/import/', views.import_data_coordinator_view, name='import_data_coordinator'),

    path('servicios/export/', views.export_data_service_view, name='export_data_service'),
    path('servicios/import/', views.import_data_service_view, name='import_data_service'),

    path('reservas/export/', views.export_data_reserve_view, name='export_data_reserve'),
    path('reservas/import/', views.import_data_reserve_view, name='import_data_reserve'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)