# Generated by Django 3.0.6 on 2020-05-29 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contact_Web', '0013_auto_20200529_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='profesion',
            field=models.CharField(max_length=50, null=True),
        ),
    ]