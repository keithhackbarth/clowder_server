# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clowder_server', '0002_auto_20150728_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alert',
            name='user',
        ),
        migrations.RemoveField(
            model_name='ping',
            name='user',
        ),
    ]
