# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-20 00:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0014_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='item',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]