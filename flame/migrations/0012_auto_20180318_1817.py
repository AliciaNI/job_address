# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-18 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flame', '0011_auto_20180318_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpositionssearchweb',
            name='search_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='search time'),
        ),
    ]
