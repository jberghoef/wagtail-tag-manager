# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 02:21
from __future__ import unicode_literals

import wagtail.core.fields
import django.db.models.deletion
from django.db import models, migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),  # noqa: E501
                ('subtitle', models.CharField(blank=True, default='', max_length=255)),
                ('body', wagtail.core.fields.RichTextField(blank=True, default='')),
            ],
            options={
                'abstract': False,
            },
            bases='wagtailcore.page',
        ),
    ]