# Generated by Django 4.2.1 on 2023-07-27 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_alter_profile_profile_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FriendRequest',
        ),
    ]
