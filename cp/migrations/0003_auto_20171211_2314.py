# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-11 23:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cp', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='referrer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='referral', to='cp.Profile', to_field='user'),
        ),
    ]
