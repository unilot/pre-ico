# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-25 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0006_lead'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
