# Generated by Django 3.0.6 on 2020-05-31 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contact_Web', '0023_auto_20200529_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='comentario_reingreso',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]