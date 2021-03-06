# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-04 16:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('cp', '0005_profile_token_amount_reserved'),
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=64)),
            ],
            options={
                'base_manager_name': '_plain_manager',
                'abstract': False,
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('_plain_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='TextTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', martor.models.MartorField()),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='cp.Text')),
            ],
            options={
                'abstract': False,
                'db_tablespace': '',
                'default_permissions': (),
                'managed': True,
                'db_table': 'cp_text_translation',
            },
        ),
        migrations.AlterUniqueTogether(
            name='texttranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
