# Generated by Django 3.2.8 on 2023-01-10 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0004_alter_film_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='film',
            options={'ordering': ['name']},
        ),
    ]
