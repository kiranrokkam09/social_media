# Generated by Django 4.1.13 on 2024-06-06 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_friend_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='request',
        ),
    ]
