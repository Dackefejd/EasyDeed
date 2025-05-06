from django.contrib import admin
from .models import DataSource, DataPreset, TransformationStep
from .forms import DataSourceForm, TransformationStepForm

"""
admin.py – Custom Django admin configuration for managing DataSource, DataPreset, and TransformationStep.

This module enhances the Django admin interface to support dynamic, configurable data workflows
by exposing rich JSON configuration fields in a user-friendly way.

Customizations include:

1. DataSourceAdmin
   - Uses a custom form (DataSourceForm) that replaces the raw JSONField (`config`) with a text area (`config_pretty`)
     for editing API/file configuration in a more readable and validated format.
   - Displays key metadata fields and makes the underlying config field read-only for reference.

2. DataPresetAdmin
   - Standard model admin with slug prepopulation based on the name field.
   - Displays ownership and timestamp fields for clarity and tracking.

3. TransformationStepAdmin
   - Uses a custom form (TransformationStepForm) to display a more intuitive JSON input field (`config_pretty`)
     with automatic validation and transformation-specific examples.
   - Adds filters and sorting by `step_type` and `preset` to allow easy categorization and management of workflows.
   - Makes the raw config read-only to prevent accidental edits outside the validated form.

The goal of this setup is to provide a low-code backend environment where users can define data pipelines
entirely through the Django admin, with clear structure, safety, and documentation built in.
"""


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    form = DataSourceForm
    list_display = ['name', 'source_type', 'owner', 'created']
    readonly_fields = ['config']  

@admin.register(DataPreset)
class DataPresetAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created', 'updated']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(TransformationStep)
class TransformationStepAdmin(admin.ModelAdmin):
    form = TransformationStepForm
    list_display = ['step_type', 'preset', 'order']
    list_filter = ['step_type', 'preset']
    ordering = ['preset__name', 'order']
    search_fields = ['preset__name', 'step_type']
    readonly_fields = ['config']
