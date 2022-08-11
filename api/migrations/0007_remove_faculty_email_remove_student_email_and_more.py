# Generated by Django 4.0.4 on 2022-08-10 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_student_batch_alter_student_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty',
            name='email',
        ),
        migrations.RemoveField(
            model_name='student',
            name='email',
        ),
        migrations.AlterField(
            model_name='faculty',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.department'),
        ),
    ]
