# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-30 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20180125_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='kind',
            field=models.CharField(choices=[('email', 'Email'), ('webhook', 'Webhook'), ('hipchat', 'HipChat'), ('slack', 'Slack'), ('pd', 'PagerDuty'), ('po', 'Pushover'), ('victorops', 'VictorOps'), ('sms', 'SMS'), ('twitter', 'Twitter'), ('telegram', 'Telegram')], max_length=20),
        ),
    ]
