# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 03:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0006_profile_followable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followable',
            field=models.CharField(default='1', max_length=1),
        ),
    ]
