# Generated by Django 5.2 on 2025-05-06 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataprep', '0005_datasource_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasource',
            name='slug',
        ),
        migrations.AddField(
            model_name='datapreset',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
