# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('code', models.CharField(default=b'', max_length=20)),
                ('gender', models.IntegerField(default=0)),
                ('age', models.IntegerField(default=0)),
                ('exp', models.IntegerField(default=0)),
                ('st_time', models.DateTimeField(null=True, blank=True)),
                ('ed_time', models.DateTimeField(null=True, blank=True)),
                ('votes', models.CommaSeparatedIntegerField(max_length=1000)),
                ('valid', models.IntegerField(default=0)),
                ('comment', models.TextField(default=b'')),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('img_id', models.IntegerField(default=0)),
                ('method1', models.IntegerField(default=0)),
                ('method2', models.IntegerField(default=0)),
                ('method3', models.IntegerField(default=0)),
                ('result', models.IntegerField(default=0)),
                ('st_time', models.DateTimeField(null=True, blank=True)),
                ('ed_time', models.DateTimeField(null=True, blank=True)),
                ('reason', models.CommaSeparatedIntegerField(default=b'0,0,0,0,0,0,0,0,0,0', max_length=20)),
                ('check', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to='userstudy.People')),
            ],
            options={
                'ordering': ['user', 'order'],
            },
            bases=(models.Model,),
        ),
    ]
