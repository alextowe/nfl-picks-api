# Generated by Django 4.2.1 on 2023-08-02 02:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0037_friendrequest_is_declined'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='declined_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
