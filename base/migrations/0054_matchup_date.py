# Generated by Django 4.2.5 on 2023-09-22 20:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0053_matchup_away_score_matchup_home_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchup',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
