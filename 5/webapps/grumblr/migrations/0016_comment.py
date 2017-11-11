# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-20 08:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0015_auto_20171019_2021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_time', models.DateTimeField(auto_now=True)),
                ('comment_content', models.CharField(max_length=100)),
                ('item', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='grumblr.Item')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
