# Generated by Django 3.0.6 on 2020-05-30 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contact_Web', '0022_auto_20200529_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='ocupacion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='profesion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]