# Generated by Django 2.1.8 on 2019-04-23 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_tag_manager', '0010_auto_20190403_0639'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='tags',
            field=models.ManyToManyField(help_text='The tags to include when this page is loaded.', to='wagtail_tag_manager.Tag'),
        ),
    ]
