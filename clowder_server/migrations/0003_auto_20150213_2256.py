# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('clowder_server', '0002_auto_20150130_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='create',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 13, 22, 56, 38, 379391), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ping',
            name='status_passing',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
