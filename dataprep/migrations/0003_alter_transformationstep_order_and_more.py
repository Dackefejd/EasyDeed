# Generated by Django 5.2 on 2025-05-06 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataprep', '0002_remove_datapreset_last_updated_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transformationstep',
            name='order',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='transformationstep',
            name='step_type',
            field=models.CharField(choices=[('drop_columns', 'Drop Columns'), ('filter_rows', 'Filter Rows'), ('reorder_columns', 'Reorder Columns'), ('rename_columns', 'Rename Columns'), ('remove_duplicates', 'Remove Duplicates'), ('add_columns', 'Add Columns')], max_length=100),
        ),
    ]
