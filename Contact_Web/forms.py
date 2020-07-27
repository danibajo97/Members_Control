from django import forms
from .models import *
from bootstrap_modal_forms.forms import BSModalForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from.funtions import cal_date_boolean


class ContactoForm(BSModalForm):

    class Meta:
        model = Contacto
        fields = '__all__'
        exclude = ['fecha_creacion_contacto', 'estado',
                   'fecha_reingreso', 'comentario_reingreso',
                   'baja_por', 'fecha_baja']

    def clean_carnet_identidad(self):
        carnet_identidad = self.cleaned_data['carnet_identidad']

        try:
            int(carnet_identidad)
        except ValueError:
            raise forms.ValidationError('Solo pueden haber números en el carnet')

        if len(carnet_identidad) != 11:
            raise forms.ValidationError('No posee los 11 dígitos')
        if cal_date_boolean(carnet_identidad) is not True:
            raise forms.ValidationError('Existe un error en la fecha del carnet')
        return carnet_identidad

class ContactoUpdateForm(BSModalForm):
    
    class Meta:
        model = Contacto
        fields = '__all__'
        exclude = ['fecha_creacion_contacto', 'estado']

    def clean_carnet_identidad(self):
        carnet_identidad = self.cleaned_data['carnet_identidad']

        try:
            int(carnet_identidad)
        except ValueError:
            raise forms.ValidationError('Solo pueden haber números en el carnet')

        if len(carnet_identidad) != 11:
            raise forms.ValidationError('No posee los 11 dígitos')
        if cal_date_boolean(carnet_identidad) is not True:
            raise forms.ValidationError('Existe un error en la fecha del carnet')
        return carnet_identidad    

class BajaForm(BSModalForm):
    fecha_baja = forms.DateField(required=True)

    class Meta:
        model = Contacto
        fields = ['fecha_baja', 'baja_por']


class ReingresoForm(BSModalForm):
    fecha_reingreso = forms.DateField(required=True)

    class Meta:
        model = Contacto
        fields = ['fecha_reingreso', 'comentario_reingreso']


class RepartoForm(BSModalForm):
    class Meta:
        model = Reparto
        fields = '__all__'
        exclude = ['fecha_creacion_reparto']


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin,
                             UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_staff']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

