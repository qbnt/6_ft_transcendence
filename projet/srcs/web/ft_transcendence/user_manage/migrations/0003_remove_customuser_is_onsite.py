# Generated by Django 3.2.25 on 2024-08-27 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0002_auto_20240815_0832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_onsite',
        ),
    ]
