# Generated by Django 3.0.6 on 2020-07-02 21:22

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('Contact_Web', '0038_auto_20200701_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='numero_celular',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=12, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='numero_fijo',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=10, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='numero_trabajo',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=12, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='numero_vecino',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=10, null=True, region=None),
        ),
    ]