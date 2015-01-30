# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clowder_server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ping',
            name='value',
            field=models.FloatField(),
            preserve_default=True,
        ),
    ]
