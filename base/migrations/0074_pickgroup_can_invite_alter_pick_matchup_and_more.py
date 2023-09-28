# Generated by Django 4.2.5 on 2023-09-28 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0073_alter_pickgroup_owner_pick'),
    ]

    operations = [
        migrations.AddField(
            model_name='pickgroup',
            name='can_invite',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='pick',
            name='matchup',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='picks_for_matchup', to='base.matchup'),
        ),
        migrations.AlterField(
            model_name='pick',
            name='pick_group',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='picks_for_group', to='base.pickgroup'),
        ),
    ]
