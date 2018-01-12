# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-12 00:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchangerate',
            name='eth_raised',
            field=models.CharField(blank=True, max_length=27, null=True),
        ),
        migrations.AddField(
            model_name='exchangerate',
            name='tokens_left',
            field=models.CharField(blank=True, max_length=27, null=True),
        ),
        migrations.AddField(
            model_name='exchangerate',
            name='total_tokens',
            field=models.CharField(blank=True, max_length=27, null=True),
        ),
    ]