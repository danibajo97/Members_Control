# Generated by Django 3.0.6 on 2020-05-23 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contact_Web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='baja_por',
            field=models.CharField(choices=[('Fallecimiento', 'Fallecimiento'), ('Traslado', 'Traslado'), ('Salida', 'Salida'), ('Disciplina', 'Disciplina')], max_length=13),
        ),
    ]
