# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clowder_account', '0003_auto_20150728_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clowderuser',
            name='public_key',
        ),
        migrations.RemoveField(
            model_name='clowderuser',
            name='secret_key',
        ),
        migrations.AlterField(
            model_name='company',
            name='public_key',
            field=shortuuidfield.fields.ShortUUIDField(db_index=True, unique=True, max_length=22, editable=False, blank=True),
        ),
    ]
