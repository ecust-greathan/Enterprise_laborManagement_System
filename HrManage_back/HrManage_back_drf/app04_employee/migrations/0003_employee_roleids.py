# Generated by Django 4.2.7 on 2024-03-07 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app04_employee', '0002_employee_correctiontime'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='roleIds',
            field=models.JSONField(blank=True, null=True),
        ),
    ]