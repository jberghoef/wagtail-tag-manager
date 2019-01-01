# Generated by Django 2.1.4 on 2018-12-27 16:23

from django.db import migrations, models
import wagtail_tag_manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_tag_manager', '0004_auto_20181206_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trigger',
            name='pattern',
            field=models.CharField(help_text="The regex pattern to match the full url path with. Groups will be added to the included tag's context.", max_length=255, validators=[wagtail_tag_manager.models.searchable_regex_validator]),
        ),
    ]