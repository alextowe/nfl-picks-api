# Generated by Django 4.2.5 on 2023-09-22 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0056_alter_matchup_week_delete_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchup',
            name='away_score',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='matchup',
            name='home_score',
            field=models.IntegerField(),
        ),
    ]