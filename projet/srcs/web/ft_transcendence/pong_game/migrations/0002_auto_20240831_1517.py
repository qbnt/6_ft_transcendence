# Generated by Django 3.2.25 on 2024-08-31 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pong_game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pongresult',
            name='date_played',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='pongresult',
            name='loser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lost_games', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pongresult',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_games', to=settings.AUTH_USER_MODEL),
        ),
    ]
