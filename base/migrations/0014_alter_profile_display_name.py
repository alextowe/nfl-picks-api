# Generated by Django 4.2.1 on 2023-06-16 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_profile_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_name',
            field=models.CharField(max_length=50),
        ),
    ]