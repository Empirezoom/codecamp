# Generated by Django 4.0.6 on 2022-07-22 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type',
            name='slug',
        ),
    ]
