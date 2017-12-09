# Generated by Django 2.0 on 2017-12-08 23:49

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import martor.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.BooleanField(default=False)),
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
            name='FAQTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', martor.models.MartorField()),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='cp.FAQ')),
            ],
            options={
                'db_table': 'cp_faq_translation',
                'managed': True,
                'abstract': False,
                'default_permissions': (),
                'db_tablespace': '',
            },
        ),
        migrations.AlterUniqueTogether(
            name='faqtranslation',
            unique_together={('language_code', 'master')},
        ),
    ]
