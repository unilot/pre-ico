# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-02 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0009_auto_20180202_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advisertranslation',
            name='full_name',
            field=models.CharField(max_length=64),
        ),
    ]
