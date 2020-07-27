from django.db.models import Q
from django.http import HttpResponse, request
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import *
from .models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import *
from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)
from .funtions import *
from .resources import ContactoResource
from tablib import Dataset
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import Table

def home(request):
    return render(request, "home.html")


def contact_list(request):
    query = Contacto.objects.filter(estado=True).order_by('pk')

    context = {'contact_list': query}
    return render(request, "miembro_list.html", context)


class CreateContact(BSModalCreateView):
    """View que crea un contacto nuevo"""

    form_class = ContactoForm
    template_name = "Contact/create_contact_modal.html"
    success_message = 'Success: Contact was created.'
    success_url = reverse_lazy('Contact_Web:MiembroList')


class UpdateContact(BSModalUpdateView):
    """View que edita un contacto"""

    model = Contacto
    pk_url_kwarg = "pk"
    context_object_name = "contact"
    form_class = ContactoUpdateForm
    success_message = 'Success: Contact was updated.'
    success_url = reverse_lazy('Contact_Web:MiembroList')
    template_name = "Contact/update_contact_modal.html"


class DeleteContact(BSModalDeleteView):
    """View para borrar un contacto"""

    model = Contacto
    pk_url_kwarg = "pk"
    context_object_name = "contact"
    template_name = "Contact/delete_contact_modal.html"
    success_message = 'Success: Contact was deleted.'
    success_url = reverse_lazy('Contact_Web:MiembroList')


class DetailContact(BSModalReadView):
    """View para ver el detalle de un contacto"""

    model = Contacto
    pk_url_kwarg = "pk"
    context_object_name = "contact"
    template_name = "Contact/detail_contact_modal.html"

    def get_object(self, queryset=None):
        obj = super(DetailContact, self).get_object()
        age = cal_age(obj.fecha_nacimiento)
        sex = cal_sex(obj.carnet_identidad)
        context = {'contact': obj, 'age': age, 'sex': sex}
        return context


def contact_baja_list(request):
    query = Contacto.objects.filter(estado=False).order_by('pk')
    context = {'contact_baja_list': query}
    return render(request, "baja_list.html", context)


class CreateContactBaja(BSModalUpdateView):
    model = Contacto
    pk_url_kwarg = "pk"
    context_object_name = "contact"
    form_class = BajaForm
    success_message = 'Success: Baja añadida.'
    template_name = "Contact/create_contact_baja_modal.html"
    success_url = reverse_lazy('Contact_Web:MiembroList')

    def get_object(self, queryset=None):
        obj = super(CreateContactBaja, self).get_object()
        return obj

    def get_success_url(self):
        obj = self.get_object()
        obj.estado = False
        obj.save()
        return self.success_url


class UpdateContactBaja(BSModalUpdateView):
    """View que edita un contacto"""

    model = Contacto
    pk_url_kwarg = "pk"
    context_object_name = "contact"
    form_class = ContactoUpdateForm
    success_message = 'Success: Baja was updated.'
    success_url = reverse_lazy('Contact_Web:BajaList')
    template_name = "Contact/update_contact_modal.html"


class DeleteContactBaja(BSModalDeleteView):
    """View para borrar un contacto"""

    model = Contacto
    pk_url_kwarg = "pk"
    context_object_name = "contact"
    template_name = "Contact/delete_contact_modal.html"
    success_message = 'Success: Baja was deleted.'
    success_url = reverse_lazy('Contact_Web:BajaList')


class RecuperarContact(BSModalUpdateView):
    model = Contacto
    pk_url_kwarg = "pk"
    context_object_name = "contact"
    form_class = ReingresoForm
    success_message = 'Success: Contacto recuperado.'
    template_name = "Contact/recuperar_contact_modal.html"
    success_url = reverse_lazy('Contact_Web:BajaList')

    def get_object(self, queryset=None):
        obj = super(RecuperarContact, self).get_object()
        return obj

    def get_success_url(self):
        obj = self.get_object()
        obj.estado = True
        obj.save()
        return self.success_url


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'Registration/signup_modal.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('Contact_Web:MiembroList')


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'Registration/login_modal.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('Contact_Web:MiembroList')


def export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        contacto_resource = ContactoResource()
        dataset = contacto_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="contact_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="contact_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="contact_data.xls"'
            return response

    return render(request, 'Contact/export.html')


def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        dataset = Dataset()
        contact_resources = ContactoResource()
        try:
            new_contact = request.FILES['importData']
        except MultiValueDictKeyError:
            return render(request, 'Alerts/import_alert.html')
        else:
            try:
                if file_format == 'CSV':
                    dataset.load(new_contact.read().decode('utf-8'), format='csv')
                    result = contact_resources.import_data(dataset, dry_run=True)
                elif file_format == 'JSON':
                    dataset.load(new_contact.read().decode('utf-8'), format='json')
                    # Testing data import
                    result = contact_resources.import_data(dataset, dry_run=True)
            except:
                return render(request, 'Alerts/import_dimensions_alert.html')
            if not result.has_errors():
                # Import now
                contact_resources.import_data(dataset, dry_run=False)

    return render(request, 'Contact/import.html')


def recuperar_all_bajas(request):
    if request.method == "POST":
        contact_list = Contacto.objects.filter(estado=False)
        for contact in contact_list:
            contact.estado = True
            contact.save()
        return redirect("Contact_Web:BajaList")
    else:
        return render(request, "Contact/recuperar_all_contact_modal.html")


def delete_all_contact(request):
    if request.method == "POST":
        contact_list = Contacto.objects.filter(estado=True).delete()
        return redirect("Contact_Web:MiembroList")
    else:
        return render(request, "Contact/delete_all_contact_modal.html")


def delete_all_contact_baja(request):
    if request.method == "POST":
        contact_list = Contacto.objects.filter(estado=False).delete()
        return redirect("Contact_Web:BajaList")
    else:
        return render(request, "Contact/delete_all_contact_baja_modal.html")


def search_contact(request):
    if request.method == 'POST':
        reparto = Reparto.objects.filter(es_reparto=True)
        contact_all = Contacto.objects.filter(estado=True)
        contact_filter = Contacto.objects.filter(estado=True)

        if request.POST['reparto'] != 'Cualquiera':
            contact_filter = contact_filter.filter(reparto__nombre_reparto=request.POST.get('reparto'))

        if request.POST['sexo'] != 'Cualquiera':
            if request.POST['sexo'] == 'Masculino':
                contact_filter = contact_filter.filter(sexo=True)
            else:
                contact_filter = contact_filter.filter(sexo=False)

        if request.POST['edad'] != 'Cualquiera':
            contact_filter = filter_age(request.POST['edad'], contact_filter)

        if request.POST['calle'] != 'Cualquiera':
            contact_filter = contact_filter.filter(calle=request.POST['calle'])
    
        if request.POST['mes'] != 'Cualquiera':
            contact_filter = filter_mes(request.POST['mes'], contact_filter)
        
        if request.POST['ingreso'] != 'Cualquiera':
            contact_filter = filter_ingreso(request.POST['ingreso'], contact_filter)
        
        if request.POST['bautismo'] != 'Cualquiera':
            contact_filter = filter_bautismo(request.POST['bautismo'], contact_filter)

        context = {'contact_list': contact_filter, 'reparto': reparto, 'contact_all': contact_all}
        return render(request, "Contact/search_contact.html", context)
    else:
        contact_all = Contacto.objects.filter(estado=True)
        reparto = Reparto.objects.filter(es_reparto=True)
        context = {'reparto': reparto, 'contact_all': contact_all}
        return render(request, "Contact/search_contact.html", context)


def report_contact(request):
    if request.method == 'POST':

        if request.POST['orden']:
            contact_filter = filter_orden(request.POST['orden'])

        if request.POST['sexo'] != 'Cualquiera':
            if request.POST['sexo'] == 'Masculino':
                contact_filter = contact_filter.filter(sexo=True)
            else:
                contact_filter = contact_filter.filter(sexo=False)

        if request.POST['edad'] != 'Cualquiera':
            contact_filter = filter_age(request.POST['edad'], contact_filter)

        if request.POST['reparto'] != '--------':
            contact_filter = contact_filter.filter(reparto__nombre_reparto=request.POST.get('reparto'))
            response = reparto_print(contact_filter)
            return response

        elif request.POST['cumpleanos'] != '--------':
            contact_filter = reporte_birthday(request.POST['cumpleanos'], contact_filter)
            response = cumpleanos_print(contact_filter)
            return response

        elif request.POST['ingreso'] != '--------':
            contact_filter = reporte_ingreso(request.POST['ingreso'], contact_filter)
            response = ingreso_print(contact_filter)
            return response

        elif request.POST['bautismo'] != '--------':
            contact_filter = reporte_bautismo(request.POST['bautismo'], contact_filter)
            response = bautismo_print(contact_filter)
            return response

        response = contact_general_print(contact_filter)
        return response
    else:
        reparto = Reparto.objects.filter(es_reparto=True)
        context = {'reparto': reparto}
        return render(request, "Contact/report_contact.html", context)


def contact_print(self):
    response = HttpResponse(content_type='application/pdf')
    buff = io.BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=landscape(letter),
                            rightMargin=20,
                            leftMargin=20,
                            topMargin=20,
                            bottomMargin=18,
                            )
    contact = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Miembros", styles['Heading1'])
    contact.append(header)
    headings = ('Id', 'Nombre', '1er Apellido', '2do Apellido', 'Carnet',
                'Fecha de Ingreso', 'Fecha de Bautismo', 'Fecha de Creacion')
    all_contacts = []
    for p in Contacto.objects.filter(estado=True).order_by('pk'):
        all_contacts.append((p.pk, p.nombre, p.primer_apellido, p.segundo_apellido, p.carnet_identidad,
                             p.fecha_ingreso, p.fecha_bautiso, p.fecha_creacion_contacto))

    t = Table([headings] + all_contacts)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (9, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

    contact.append(t)
    doc.build(contact)
    response.write(buff.getvalue())
    buff.close()
    return response


def contact_baja_print(self):
    response = HttpResponse(content_type='application/pdf')
    buff = io.BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=landscape(letter),
                            rightMargin=20,
                            leftMargin=20,
                            topMargin=20,
                            bottomMargin=18,
                            )
    contact = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Bajas", styles['Heading1'])
    contact.append(header)
    headings = ('Id', 'Nombre', '1er Apellido', '2do Apellido', 'Carnet',
                'Baja Por', 'Fecha de Baja', 'Fecha de Creacion')

    all_contacts = [(p.pk, p.nombre, p.primer_apellido, p.segundo_apellido, p.carnet_identidad,
                     p.baja_por, p.fecha_baja, p.fecha_creacion_contacto)
                    for p in Contacto.objects.filter(estado=False).order_by('pk')]

    t = Table([headings] + all_contacts)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (8, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

    contact.append(t)
    doc.build(contact)
    response.write(buff.getvalue())
    buff.close()
    return response


def about_page(request):
    return render(request, 'Contact/about_contact.html')


def dashboard(request):
    all_contact = len(Contacto.objects.filter(estado=True))
    all_bajas = len(Contacto.objects.filter(estado=False))
    all_repartos = len(Reparto.objects.filter(es_reparto=True))
    context = {'all_contact': all_contact, 'all_bajas': all_bajas, 'all_repartos': all_repartos}

    return render(request, 'Contact/dashboard_contact.html', context)


# Reparto Views
def reparto_list(request):
    query = Reparto.objects.order_by('pk')

    context = {'reparto_list': query}
    return render(request, 'Repartos/reparto_list.html', context)


class CreateReparto(BSModalCreateView):
    """View que crea un reparto nuevo"""

    form_class = RepartoForm
    template_name = "Repartos/create_reparto_modal.html"
    success_message = 'Success: Reparto was created.'
    success_url = reverse_lazy('Contact_Web:RepartoList')


class UpdateReparto(BSModalUpdateView):
    """View que edita un reparto"""

    model = Reparto
    pk_url_kwarg = "pk"
    context_object_name = "reparto"
    form_class = RepartoForm
    success_message = 'Success: Reparto was updated.'
    success_url = reverse_lazy('Contact_Web:RepartoList')
    template_name = "Repartos/update_reparto_modal.html"


class DeleteReparto(BSModalDeleteView):
    """View para borrar un reparto"""

    model = Reparto
    pk_url_kwarg = "pk"
    context_object_name = "reparto"
    template_name = "Repartos/delete_reparto_modal.html"
    success_message = 'Success: Reparto was deleted.'
    success_url = reverse_lazy('Contact_Web:RepartoList')


class DetailReparto(BSModalReadView):
    """View para ver el detalle de un reparto"""

    model = Reparto
    pk_url_kwarg = "pk"
    context_object_name = "reparto"
    template_name = "Repartos/detail_reparto_modal.html"


def delete_all_reparto(request):
    if request.method == "POST":
        reparto_list = Reparto.objects.delete()
        return redirect("Contact_Web:RepartoList")
    else:
        return render(request, "Repartos/delete_all_repartos_modal.html")
