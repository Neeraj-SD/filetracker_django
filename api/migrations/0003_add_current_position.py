# Generated by Django 4.0.4 on 2022-05-05 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_faculty_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='faculty',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.role'),
        ),
        migrations.AlterField(
            model_name='position',
            name='remarks',
            field=models.CharField(blank=True, max_length=3000),
        ),
        migrations.AlterField(
            model_name='position',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='api.request'),
        ),
        migrations.AlterField(
            model_name='position',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('F', 'Forwarded'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1),
        ),
        migrations.CreateModel(
            name='CurrentPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.position')),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.request')),
            ],
        ),
    ]
