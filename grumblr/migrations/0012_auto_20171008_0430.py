# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 08:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0011_auto_20171008_0358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='profile_image/default.png', upload_to='profile_image'),
        ),
    ]