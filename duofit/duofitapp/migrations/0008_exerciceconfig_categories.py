# Generated by Django 5.0 on 2024-01-03 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duofitapp', '0007_alter_exercicelog_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciceconfig',
            name='categories',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
