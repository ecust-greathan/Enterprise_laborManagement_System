# Generated by Django 4.2.7 on 2024-02-27 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app02_roles', '0001_initial'),
        ('app01_index', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='role',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='app02_roles.roles', verbose_name='用户角色'),
        ),
    ]
