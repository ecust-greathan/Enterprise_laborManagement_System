# Generated by Django 4.2.7 on 2024-03-06 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app04_employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='correctionTime',
            field=models.DateField(blank=True, null=True),
        ),
    ]