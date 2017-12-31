# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-31 14:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import landing.models
import preico.validators


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0004_auto_20171231_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.BooleanField(default=False)),
                ('linkedin_nickname', models.SlugField(allow_unicode=True, max_length=64)),
                ('photo', models.ImageField(upload_to=landing.models.TeamMember.__get_photo_path__, validators=[preico.validators.ImageMinSizeValidator(min_height=150, min_width=150)])),
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
            name='TeamMemberTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=32)),
                ('position', models.CharField(max_length=128)),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='landing.TeamMember')),
            ],
            options={
                'abstract': False,
                'managed': True,
                'db_table': 'landing_teammember_translation',
                'default_permissions': (),
                'db_tablespace': '',
            },
        ),
        migrations.AlterField(
            model_name='adviser',
            name='linkedin_nickname',
            field=models.SlugField(allow_unicode=True, max_length=64),
        ),
        migrations.AlterUniqueTogether(
            name='teammembertranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
