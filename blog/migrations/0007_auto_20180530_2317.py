# Generated by Django 2.0.5 on 2018-05-30 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20180530_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readnum',
            name='blog',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Blog'),
        ),
    ]