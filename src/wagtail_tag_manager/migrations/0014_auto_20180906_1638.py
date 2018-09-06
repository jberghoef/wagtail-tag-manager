# Generated by Django 2.0.6 on 2018-09-06 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_tag_manager', '0013_auto_20180905_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='active',
            field=models.BooleanField(default=True, help_text='Uncheck to disable this tag from being included, or when using a trigger to include this tag.'),
        ),
    ]
