# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flame', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tab8',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('tab8_id', models.CharField(max_length=30)),
                ('tab8_name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='tab9',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('tab8_id', models.CharField(max_length=30)),
                ('tab9_name', models.CharField(max_length=150)),
            ],
        ),
        migrations.DeleteModel(
            name='tab1',
        ),
        migrations.DeleteModel(
            name='tab2',
        ),
    ]
