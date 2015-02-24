# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import shortuuid
import shortuuidfield.fields

def forwards_func(apps, schema_editor):
    ClowderUser = apps.get_model("clowder_account", "ClowderUser")
    db_alias = schema_editor.connection.alias
    users = ClowderUser.objects.all()
    for user in users:
        user.public_key = shortuuid.uuid()
        user.secret_key = shortuuid.uuid()
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('clowder_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clowderuser',
            name='public_key',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22),
        ),
        migrations.AddField(
            model_name='clowderuser',
            name='secret_key',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22),
        ),
        migrations.RunPython(
            forwards_func,
        ),
    ]
