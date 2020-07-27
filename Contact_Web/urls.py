from django.urls import path
from . import views
from django.conf import settings

app_name = 'Contact_Web'

urlpatterns = [

    path('', views.home, name='Home'),
    path('dashboard/', views.dashboard, name='Dashboard'),
    path('listado_miembro/', views.contact_list, name='MiembroList'),
    path('nuevo_miembro/', views.CreateContact.as_view(), name='CreateContact'),
    path('detalle_miembro/<int:pk>/', views.DetailContact.as_view(), name='DetailContact'),
    path('editar_miembro/<int:pk>/', views.UpdateContact.as_view(), name='UpdateContact'),
    path('borrar_miembro/<int:pk>/', views.DeleteContact.as_view(), name='DeleteContact'),
    path('borrar_todos/', views.delete_all_contact, name='DeleteAllContact'),
    path('borrar_todos_baja/', views.delete_all_contact_baja, name='DeleteAllContactBaja'),
    path('recuperar_todos_baja/', views.recuperar_all_bajas, name='RecuperarAllBajas'),

    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),

    path('listado_baja/', views.contact_baja_list, name='BajaList'),
    path('baja/<int:pk>/', views.CreateContactBaja.as_view(), name='CreateContactBaja'),
    path('editar_baja/<int:pk>/', views.UpdateContactBaja.as_view(), name='UpdateContactBaja'),
    path('borrar_baja/<int:pk>/', views.DeleteContactBaja.as_view(), name='DeleteContactBaja'),
    path('recuperar_miembro/<int:pk>/', views.RecuperarContact.as_view(), name='RecuperarContact'),

    path('busqueda_avanzada/', views.search_contact, name='SearchContact'),
    path('importar/', views.import_data, name='Import'),
    path('exportar/', views.export_data, name='Export'),
    path('reporte/', views.report_contact, name='Report'),

    path('miembro/print', views.contact_print, name='ContactPrint'),
    path('baja/print', views.contact_baja_print, name='ContactBajaPrint'),

    path('acerca_de/', views.about_page, name='AboutPage'),

    # reparto urls
    path('listado_reparto/', views.reparto_list, name='RepartoList'),
    path('nuevo_reparto/', views.CreateReparto.as_view(), name='CreateReparto'),
    path('detalle_reparto/<int:pk>/', views.DetailReparto.as_view(), name='DetailReparto'),
    path('editar_reparto/<int:pk>/', views.UpdateReparto.as_view(), name='UpdateReparto'),
    path('borrar_reparto/<int:pk>/', views.DeleteReparto.as_view(), name='DeleteReparto'),
    path('borrar_todos_repartos/', views.delete_all_reparto, name='DeleteAllReparto'),
]



