# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clowder_server', '0003_auto_20150729_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='ping',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
