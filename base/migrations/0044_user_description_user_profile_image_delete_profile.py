# Generated by Django 4.2.5 on 2023-09-17 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0043_rename_was_canceled_friendrequest_is_canceled'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='base/images/'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]