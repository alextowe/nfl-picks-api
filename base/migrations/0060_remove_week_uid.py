# Generated by Django 4.2.5 on 2023-09-23 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0059_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='week',
            name='uid',
        ),
    ]
