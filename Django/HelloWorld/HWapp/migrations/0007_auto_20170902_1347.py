# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-02 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HWapp', '0006_auto_20170902_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hwapp',
            name='dianhua',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hwapp',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='hwapp',
            name='qq',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
