from datetime import *
from django.http import HttpResponse

from .models import *
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import *
from reportlab.platypus import Table


def cal_date_boolean(dni):
    s_year = dni[0:2]
    top_year = ['20', s_year]
    full_year = int("".join(top_year))
    today_year = datetime.today().year

    if full_year >= today_year:
        top_year = ['19', s_year]
        full_year = int("".join(top_year))

    month = int(dni[2:4])
    day = int(dni[4:6])
    try:
        birthday = date(full_year, month, day)
    except ValueError:
        return False    
    return True


def cal_age(birthday):
    today = datetime.now()
    rectifier = datetime(today.year, birthday.month, birthday.day) >= today
    return today.year - birthday.year - rectifier


def cal_sex(dni):
    sex = int(dni[9])
    if sex % 2 == 0:
        return "Masculino"
    else:
        return "Femenino"


def filter_age(edad, contact_filter):
    today = datetime.now()
    if edad == 'Ancianos (65 - adelante)':
        start_date = datetime(today.year-95, today.month, today.day)
        end_date = datetime(today.year-65, today.month, today.day)
        contact_filter = contact_filter.filter(fecha_nacimiento__range=(start_date, end_date))
    if edad == 'Adultos (47 - 59)':
        start_date = datetime(today.year-59, today.month, today.day)
        end_date = datetime(today.year-47, today.month, today.day)
        contact_filter = contact_filter.filter(fecha_nacimiento__range=(start_date, end_date))
    if edad == 'Adultos Jovenes (35 - 46)':
        start_date = datetime(today.year-46, today.month, today.day)
        end_date = datetime(today.year-35, today.month, today.day)
        contact_filter = contact_filter.filter(fecha_nacimiento__range=(start_date, end_date))
    if edad == 'Jovenes Adultos (24 - 34)':
        start_date = datetime(today.year-34, today.month, today.day)
        end_date = datetime(today.year-24, today.month, today.day)
        contact_filter = contact_filter.filter(fecha_nacimiento__range=(start_date, end_date))
    if edad == 'Jovenes (15 - 24)':
        start_date = datetime(today.year-24, today.month, today.day)
        end_date = datetime(today.year-15, today.month, today.day)
        contact_filter = contact_filter.filter(fecha_nacimiento__range=(start_date, end_date))
    if edad == 'Juveniles (13 - 15)':
        start_date = datetime(today.year-15, today.month, today.day)
        end_date = datetime(today.year-13, today.month, today.day)
        contact_filter = contact_filter.filter(fecha_nacimiento__range=(start_date, end_date))    
    if edad == 'Primarios (8 - 12)':
        start_date = datetime(today.year-12, today.month, today.day)
        end_date = datetime(today.year-8, today.month, today.day)
        contact_filter = contact_filter.filter(fecha_nacimiento__range=(start_date, end_date))        
    return contact_filter


def filter_mes(mes, contact_filter):
    if mes == 'Enero':
        contact_filter = contact_filter.filter(fecha_nacimiento__month=1)
    if mes == 'Febrero':
        contact_filter = contact_filter.filter(fecha_nacimiento__month=2)
    if mes == 'Marzo':
        contact_filter = contact_filter.filter(fecha_nacimiento__month=3)
    if mes == 'Abril':
       contact_filter = contact_filter.filter(fecha_nacimiento__month=4)
    if mes == 'Mayo':
        contact_filter = contact_filter.filter(fecha_nacimiento__month=5)
    if mes == 'Junio':
       contact_filter = contact_filter.filter(fecha_nacimiento__month=6)
    if mes == 'Julio':
        contact_filter = contact_filter.filter(fecha_nacimiento__month=7)
    if mes == 'Agosto':
       contact_filter = contact_filter.filter(fecha_nacimiento__month=8)
    if mes == 'Septiembre':
        contact_filter = contact_filter.filter(fecha_nacimiento__month=9)
    if mes == 'Octubre':
        contact_filter = contact_filter.filter(fecha_nacimiento__month=10)
    if mes == 'Noviembre':
        contact_filter = contact_filter.filter(fecha_nacimiento__month=11)
    if mes == 'Diciembre':
        contact_filter = contact_filter.filter(fecha_nacimiento__month=12)
    return contact_filter


def filter_orden(orden):
    if orden == 'A-Z':
        return Contacto.objects.filter(estado=True).order_by('nombre')
    else:
        return Contacto.objects.filter(estado=True).order_by('-nombre')


def filter_ingreso(ingreso, contact_filter):
    if ingreso == 'Antes - 1950':
        start_date = datetime(1930, 1, 1)
        end_date = datetime(1950, 1, 1)
        contact_filter = contact_filter.filter(fecha_ingreso__range=(start_date, end_date))
    if ingreso == '1950 - 1960':
        start_date = datetime(1950, 1, 1)
        end_date = datetime(1960, 1, 1)
        contact_filter = contact_filter.filter(fecha_ingreso__range=(start_date, end_date))
    if ingreso == '1960 - 1970':
        start_date = datetime(1960, 1, 1)
        end_date = datetime(1970, 1, 1)
        contact_filter = contact_filter.filter(fecha_ingreso__range=(start_date, end_date))
    if ingreso == '1970 - 1980':
        start_date = datetime(1970, 1, 1)
        end_date = datetime(1980, 1, 1)
        contact_filter = contact_filter.filter(fecha_ingreso__range=(start_date, end_date))
    if ingreso == '1980 - 1990':
        start_date = datetime(1980, 1, 1)
        end_date = datetime(1990, 1, 1)
        contact_filter = contact_filter.filter(fecha_ingreso__range=(start_date, end_date))
    if ingreso == '1990 - 2000':
        start_date = datetime(1990, 1, 1)
        end_date = datetime(2000, 1, 1)
        contact_filter = contact_filter.filter(fecha_ingreso__range=(start_date, end_date))
    if ingreso == '2000 - 2010':
        start_date = datetime(2000, 1, 1)
        end_date = datetime(2010, 1, 1)
        contact_filter = contact_filter.filter(fecha_ingreso__range=(start_date, end_date))
    if ingreso == '2010 - 2020':
        start_date = datetime(2010, 1, 1)
        end_date = datetime(2020, 1, 1)
        contact_filter = contact_filter.filter(fecha_ingreso__range=(start_date, end_date))
    if ingreso == '2020 - Actualidad':
        start_date = datetime(2020, 1, 1)
        end_date = datetime.now()
        contact_filter = contact_filter.filter(fecha_ingreso__range=(start_date, end_date))
    return contact_filter


def filter_bautismo(bautismo, contact_filter):
    if bautismo == 'Antes - 1950':
        start_date = datetime(1930, 1, 1)
        end_date = datetime(1950, 1, 1)
        contact_filter = contact_filter.filter(fecha_bautiso__range=(start_date, end_date))
    if bautismo == '1950 - 1960':
        start_date = datetime(1950, 1, 1)
        end_date = datetime(1960, 1, 1)
        contact_filter = contact_filter.filter(fecha_bautiso__range=(start_date, end_date))
    if bautismo == '1960 - 1970':
        start_date = datetime(1960, 1, 1)
        end_date = datetime(1970, 1, 1)
        contact_filter = contact_filter.filter(fecha_bautiso__range=(start_date, end_date))
    if bautismo == '1970 - 1980':
        start_date = datetime(1970, 1, 1)
        end_date = datetime(1980, 1, 1)
        contact_filter = contact_filter.filter(fecha_bautiso__range=(start_date, end_date))
    if bautismo == '1980 - 1990':
        start_date = datetime(1980, 1, 1)
        end_date = datetime(1990, 1, 1)
        contact_filter = contact_filter.filter(fecha_bautiso__range=(start_date, end_date))
    if bautismo == '1990 - 2000':
        start_date = datetime(1990, 1, 1)
        end_date = datetime(2000, 1, 1)
        contact_filter = contact_filter.filter(fecha_bautiso__range=(start_date, end_date))
    if bautismo == '2000 - 2010':
        start_date = datetime(2000, 1, 1)
        end_date = datetime(2010, 1, 1)
        contact_filter = contact_filter.filter(fecha_bautiso__range=(start_date, end_date))
    if bautismo == '2010 - 2020':
        start_date = datetime(2010, 1, 1)
        end_date = datetime(2020, 1, 1)
        contact_filter = contact_filter.filter(fecha_bautiso__range=(start_date, end_date))
    if bautismo == '2020 - Actualidad':
        start_date = datetime(2020, 1, 1)
        end_date = datetime.now()
        contact_filter = contact_filter.filter(fecha_bautiso__range=(start_date, end_date))
    return contact_filter


def reporte_birthday(birthday, contact_filter):
    if birthday == 'Nuevos a Viejos':
        contact_filter = contact_filter.order_by('fecha_nacimiento')
    else:
        contact_filter = contact_filter.order_by('-fecha_nacimiento')
    return contact_filter


def reporte_ingreso(ingreso, contact_filter):
    if ingreso == 'Nuevos a Viejos':
        contact_filter = contact_filter.order_by('fecha_ingreso')
    else:
        contact_filter = contact_filter.order_by('-fecha_ingreso')
    return contact_filter


def reporte_bautismo(bautismo, contact_filter):
    if bautismo == 'Nuevos a Viejos':
        contact_filter = contact_filter.order_by('fecha_bautiso')
    else:
        contact_filter = contact_filter.order_by('-fecha_bautiso')
    return contact_filter


def reparto_print(contact_filter):
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
    header = Paragraph("Reporte por Repartos", styles['Heading1'])
    contact.append(header)
    headings = ('Nombre', '1er Apellido', 'Reparto', 'Numero', 'Calle',
                'Calle Primera', 'Calle Segunda')
    all_contacts = [(p.nombre, p.primer_apellido, p.reparto.nombre_reparto, p.numero_casa, p.calle,
                     p.entre_calle_primera, p.entre_calle_segunda)
                    for p in contact_filter]

    t = Table([headings] + all_contacts)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (7, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

    contact.append(t)
    doc.build(contact)
    response.write(buff.getvalue())
    buff.close()
    return response


def cumpleanos_print(contact_filter):
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
    header = Paragraph("Reporte por Fecha de Nacimiento", styles['Heading1'])
    contact.append(header)
    headings = ('Id', 'Nombre', '1er Apellido', '2do Apellido', 'Fecha de Nacimiento', 'Sexo', 'Edad')
    all_contacts = [(p.pk, p.nombre, p.primer_apellido, p.segundo_apellido, p.fecha_nacimiento,
                     cal_sex(p.carnet_identidad), cal_age(p.fecha_nacimiento))
                    for p in contact_filter]

    t = Table([headings] + all_contacts)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (7, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

    contact.append(t)
    doc.build(contact)
    response.write(buff.getvalue())
    buff.close()
    return response


def ingreso_print(contact_filter):
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
    header = Paragraph("Reporte por Ingreso", styles['Heading1'])
    contact.append(header)
    headings = ('Id', 'Nombre', '1er Apellido', '2do Apellido', 'Fecha de Ingreso', 'Ingresa Por')
    all_contacts = [(p.pk, p.nombre, p.primer_apellido, p.segundo_apellido, p.fecha_ingreso, p.ingresa_por)
                    for p in contact_filter]

    t = Table([headings] + all_contacts)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

    contact.append(t)
    doc.build(contact)
    response.write(buff.getvalue())
    buff.close()
    return response


def bautismo_print(contact_filter):
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
    header = Paragraph("Reporte por Fecha de Bautismo", styles['Heading1'])
    contact.append(header)
    headings = ('Id', 'Nombre', '1er Apellido', '2do Apellido', 'Fecha del Bautismo', 'Local', 'Pastor')
    all_contacts = [(p.pk, p.nombre, p.primer_apellido, p.segundo_apellido,
                     p.fecha_bautiso, p.local_bautiso, p.nombre_pastor_bautiso)
                    for p in contact_filter]

    t = Table([headings] + all_contacts)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (7, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

    contact.append(t)
    doc.build(contact)
    response.write(buff.getvalue())
    buff.close()
    return response


def contact_general_print(contact_filter):
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
    header = Paragraph("Reporte General", styles['Heading1'])
    contact.append(header)
    headings = ('Id', 'Nombre', '1er Apellido', '2do Apellido', 'Carnet de Identidad')
    all_contacts = [(p.pk, p.nombre, p.primer_apellido, p.segundo_apellido,
                     p.carnet_identidad)
                    for p in contact_filter]

    t = Table([headings] + all_contacts)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (5, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

    contact.append(t)
    doc.build(contact)
    response.write(buff.getvalue())
    buff.close()
    return response