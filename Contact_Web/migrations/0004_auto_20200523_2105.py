# Generated by Django 3.0.6 on 2020-05-24 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contact_Web', '0003_auto_20200523_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='fecha_reingreso',
            field=models.DateField(null=True),
        ),
    ]