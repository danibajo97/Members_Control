from django.db import models
from datetime import *


class Reparto(models.Model):
    nombre_reparto = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=10)
    ciudad = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    es_reparto = models.BooleanField(default=True)
    fecha_creacion_reparto = models.DateField(auto_now_add=True, auto_now=False)

    def fullName(self):
        string = "{0}, ({1})"
        return string.format(self.nombre_reparto, self.municipio)

    def __str__(self):
        return self.fullName()

    class Meta:
        verbose_name_plural = 'Reparto'
        ordering = ['nombre_reparto']


class Contacto(models.Model):
    # identidad
    nombre = models.CharField(max_length=50)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, null=True, blank=True)
    carnet_identidad = models.CharField(max_length=11, unique=True)
    sexo = models.BooleanField(null=True, blank=True, default=1)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    # contactar
    numero_fijo = models.CharField(max_length=10, null=True, blank=True)
    numero_vecino = models.CharField(max_length=10, blank=True, null=True)
    numero_celular = models.CharField(max_length=12, blank=True, null=True)
    numero_trabajo = models.CharField(max_length=12, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    # direccion
    reparto = models.ForeignKey(Reparto, on_delete=models.CASCADE, null=True, blank=True)
    numero_casa = models.CharField(max_length=20, blank=True, null=True)
    edificio = models.CharField(max_length=20, null=True, blank=True)
    calle = models.CharField(max_length=50, blank=True, null=True)
    entre_calle_primera = models.CharField(max_length=50, blank=True, null=True)
    entre_calle_segunda = models.CharField(max_length=50, blank=True, null=True)
    # bautismo
    fecha_bautiso = models.DateField(blank=True, null=True)
    local_bautiso = models.CharField(max_length=30, blank=True, null=True)
    nombre_pastor_bautiso = models.CharField(max_length=80, blank=True, null=True)
    ingresa_opciones = (
    ('Examen', 'Examen'), ('Testimonio', 'Testimonio'), ('Carta', 'Carta'), ('Bautismo', 'Bautismo'))
    # ingreso
    ingresa_por = models.CharField(max_length=10, choices=ingresa_opciones, blank=True, null=True)
    fecha_ingreso = models.DateField(blank=True, null=True)
    # trabajo
    profesion = models.CharField(max_length=50, null=True, blank=True)
    ocupacion = models.CharField(max_length=50, null=True, blank=True)
    # extra
    foto = models.ImageField(blank=True, null=True, upload_to='Photos/')
    comentario_extra = models.TextField(max_length=200, null=True, blank=True)
    fecha_creacion_contacto = models.DateField(auto_now_add=True, auto_now=False)

    estado = models.BooleanField(default=True)

    fecha_reingreso = models.DateField(null=True, blank=True)
    comentario_reingreso = models.TextField(max_length=200, null=True, blank=True)

    baja_opciones = (
    ('Fallecimiento', 'Fallecimiento'), ('Traslado', 'Traslado'), ('Salida', 'Salida'), ('Disciplina', 'Disciplina'))
    baja_por = models.CharField(max_length=13, choices=baja_opciones, null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{} {} {}'.format(self.nombre, self.primer_apellido, self.segundo_apellido)

    class Meta:
        verbose_name_plural = 'Contactos'

    def save(self, *args, **kwargs):
        self.sexo = int(self.carnet_identidad[9]) % 2 == 0
        self.fecha_nacimiento = cal_date(self.carnet_identidad)
        super(Contacto, self).save(*args, **kwargs)

def cal_date(dni):
    s_year = dni[0:2]
    top_year = ['20', s_year]
    full_year = int("".join(top_year))
    today_year = datetime.today().year

    if full_year >= today_year:
        top_year = ['19', s_year]
        full_year = int("".join(top_year))

    month = int(dni[2:4])
    day = int(dni[4:6])
    birthday = date(full_year, month, day)
    return birthday