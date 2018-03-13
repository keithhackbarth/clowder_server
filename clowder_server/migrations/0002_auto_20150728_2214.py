# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clowder_account', '0003_auto_20150728_2214'),
        ('clowder_server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='company',
            field=models.ForeignKey(to='clowder_account.Company', null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='ping',
            name='company',
            field=models.ForeignKey(to='clowder_account.Company', null=True, on_delete=models.CASCADE),
        ),
        migrations.RunSQL("""
        UPDATE clowder_server_ping SET company_id = clowder_account_clowderuser.company_id
        FROM clowder_account_clowderuser
        WHERE clowder_account_clowderuser.id = clowder_server_ping.user_id;
        """),
        migrations.RunSQL("""
        UPDATE clowder_server_alert SET company_id = clowder_account_clowderuser.company_id
        FROM clowder_account_clowderuser
        WHERE clowder_account_clowderuser.id = clowder_server_alert.user_id;
        """),
    ]
