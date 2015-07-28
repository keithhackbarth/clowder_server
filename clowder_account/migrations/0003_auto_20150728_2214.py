# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clowder_account', '0002_auto_20150224_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('public_key', shortuuidfield.fields.ShortUUIDField(db_index=True, max_length=22, editable=False, blank=True)),
                ('secret_key', shortuuidfield.fields.ShortUUIDField(max_length=22, editable=False, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='clowderuser',
            name='company',
            field=models.ForeignKey(to='clowder_account.Company', null=True),
        ),
        migrations.RunSQL("""
        INSERT INTO clowder_account_company (public_key, secret_key)
        SELECT public_key, secret_key
        FROM clowder_account_clowderuser
        WHERE email != 'keith@parkme.com';
        """),
        migrations.RunSQL("""
        UPDATE clowder_account_clowderuser SET company_id = clowder_account_company.id
        FROM clowder_account_company
        WHERE clowder_account_company.public_key = clowder_account_clowderuser.public_key;
        """),
    ]
