# Generated by Django 2.0.5 on 2018-05-29 14:50

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180528_2009'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-last_updated_time']},
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='blog',
            name='created_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='blog',
            name='last_updated_time',
            field=models.DateTimeField(),
        ),
    ]
