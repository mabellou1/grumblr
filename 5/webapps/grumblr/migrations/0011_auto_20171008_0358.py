# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0010_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, upload_to='grumblr/static/grumblr/images/'),
        ),
    ]
