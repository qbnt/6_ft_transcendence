# Generated by Django 3.2.25 on 2024-08-27 16:23

from django.conf import settings
from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('live_chat', '0037_alter_chatgroup_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='group_name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=128, unique=True),
        ),
        migrations.CreateModel(
            name='OnlineUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users_online', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
