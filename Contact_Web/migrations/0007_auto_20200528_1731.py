# Generated by Django 3.0.6 on 2020-05-28 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contact_Web', '0006_auto_20200528_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='fecha_baja',
            field=models.DateField(blank=True, null=True),
        ),
    ]
