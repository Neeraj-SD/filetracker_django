# Generated by Django 4.0.4 on 2022-08-10 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_user_is_faculty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
    ]
