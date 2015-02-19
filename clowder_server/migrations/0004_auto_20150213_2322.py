# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clowder_server', '0003_auto_20150213_2256'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClowderUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('first_name', models.CharField(max_length=30, blank=True)),
                ('last_name', models.CharField(max_length=30, blank=True)),
                ('email', models.EmailField(unique=True, max_length=75, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='alert',
            name='expire_at',
        ),
        migrations.AddField(
            model_name='alert',
            name='notify_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
