# Generated by Django 2.2 on 2020-08-09 17:17

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20200808_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Текст статьи'),
        ),
    ]
