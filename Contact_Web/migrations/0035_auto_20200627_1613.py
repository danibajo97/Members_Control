# Generated by Django 3.0.6 on 2020-06-27 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contact_Web', '0034_auto_20200627_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contacto',
            name='sexo',
            field=models.BooleanField(blank=True, default=1, null=True),
        ),
    ]