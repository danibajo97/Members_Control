# Generated by Django 3.0.6 on 2020-05-28 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contact_Web', '0005_auto_20200523_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='fecha_baja',
            field=models.DateField(null=True),
        ),
    ]
