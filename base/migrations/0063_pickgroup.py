# Generated by Django 4.2.5 on 2023-09-24 02:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0062_delete_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='PickGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('members', models.ManyToManyField(blank=True, related_name='pick_groups', to=settings.AUTH_USER_MODEL)),
                ('owner', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_of', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
