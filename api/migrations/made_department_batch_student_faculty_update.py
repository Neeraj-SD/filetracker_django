# Generated by Django 4.0.4 on 2022-05-01 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='batch',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='faculty',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.department'),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.role'),
        ),
        migrations.AlterField(
            model_name='student',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.batch'),
        ),
        migrations.AlterField(
            model_name='student',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.department'),
        ),
    ]
