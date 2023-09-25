# Generated by Django 4.2.1 on 2023-08-03 02:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0038_friendrequest_declined_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='canceled_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
    ]