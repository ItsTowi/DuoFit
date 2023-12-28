# Generated by Django 5.0 on 2023-12-28 12:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciceConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday_goal', models.IntegerField()),
                ('tuesday_goal', models.IntegerField()),
                ('wednesday_goal', models.IntegerField()),
                ('thursday_goal', models.IntegerField()),
                ('friday_goal', models.IntegerField()),
                ('saturday_goal', models.IntegerField()),
                ('sunday_goal', models.IntegerField()),
                ('weekly_goal', models.IntegerField()),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
