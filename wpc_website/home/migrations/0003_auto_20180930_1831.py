# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-30 13:01
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_footertext'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='social_board_body',
            field=models.TextField(blank=True, help_text='Text to displayed just below the social board section.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='social_board_title',
            field=models.CharField(blank=True, help_text='Title to displayed for social board section.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='footertext',
            name='f_body',
            field=wagtail.core.fields.RichTextField(verbose_name='Body'),
        ),
        migrations.AlterField(
            model_name='footertext',
            name='f_title',
            field=models.CharField(help_text='Text to displayed as footer title.', max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='quote_for_the_day',
            field=models.CharField(default='Some Quote', max_length=200),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='vision_body',
            field=models.TextField(max_length=200),
        ),
    ]