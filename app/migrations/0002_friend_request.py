# Generated by Django 4.1.13 on 2024-06-06 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='request',
            field=models.BooleanField(default=False),
        ),
    ]