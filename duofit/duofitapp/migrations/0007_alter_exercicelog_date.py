# Generated by Django 5.0 on 2023-12-31 09:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duofitapp', '0006_alter_exercicelog_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercicelog',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]