# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstudy', '0007_auto_20250519_0402'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='swap_display',
            field=models.BooleanField(default=False),
        ),
    ]
