# Generated by Django 3.0.6 on 2020-05-29 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contact_Web', '0021_auto_20200529_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='numero_casa',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]