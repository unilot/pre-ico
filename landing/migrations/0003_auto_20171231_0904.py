# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-31 09:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import landing.models
import preico.validators


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_auto_20171231_0128'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roadshow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': '_plain_manager',
            },
            bases=(landing.models.AdvancedImageFieldsProcessingModelMixin, models.Model, landing.models.ResizableImageFieldMixin),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('_plain_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='RoadshowTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=64)),
                ('location', models.CharField(max_length=32, null=True)),
                ('cover_image', models.ImageField(upload_to=landing.models.Roadshow.__get_cover_image_path__, validators=[preico.validators.ImageMinSizeValidator(min_height=353, min_width=627)])),
                ('info_url', models.URLField()),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='landing.Roadshow')),
            ],
            options={
                'abstract': False,
                'db_tablespace': '',
                'db_table': 'landing_roadshow_translation',
                'default_permissions': (),
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='roadshowtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]