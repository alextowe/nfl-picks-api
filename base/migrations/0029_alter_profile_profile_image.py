# Generated by Django 4.2.1 on 2023-06-18 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default=None, upload_to='base/images/'),
        ),
    ]
