from django import forms
from django.core.exceptions import ValidationError
from .models import DataSource, DataPreset, TransformationStep
import json


"""
forms.py – Custom Django ModelForms to improve admin handling of DataSource and TransformationStep.

This file contains two custom forms:

1. DataSourceForm
- Used in admin to handle the configuration (JSON) of a data source.
- Instead of exposing the raw JSON field (`config`), an intermediate field (`config_pretty`)
is used to provide a more user-friendly text field with examples and validation.
- This allows the user to paste and edit API/file settings in a readable format.

2. TransformationStepForm
- Used in admin to create and manage transformation steps associated with a DataPreset.
- Just like for DataSource, a `config_pretty` field is used instead of the raw `config` field.
- The form also includes examples of how the configuration should look depending on the step type
(e.g. to rename columns, remove columns, filter rows, etc.).
- JSON validation is done directly in the form to prevent input errors.

The purpose of these forms is to make it easier and safer for users (via admin) to create reusable data routines - without having to understand Django models or internal JSON handling.
"""

# ──────────────── DataSourceForm ────────────────

class DataSourceForm(forms.ModelForm):
    config_pretty = forms.CharField(
        label="Settings (JSON format)",
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        help_text=(
            "Enter API configuration in JSON format.<br>"
            "Example:<br>"
            "<pre>{\n"
            ' "url": "https://dummyjson.com/carts",\n'
            ' "method": "GET",\n'
            ' "root_key": "carts",\n'
            ' "record_path": "products",\n'
            ' "meta_fields": ["userId"]\n'
            "}</pre>"
        )
    )

    class Meta:
        model = DataSource
        fields = ['name', 'owner', 'source_type']  # config is managed via config_pretty

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.config:
            self.fields['config_pretty'].initial = json.dumps(self.instance.config, indent=2)

    def clean_config_pretty(self):
        try:
            return json.loads(self.cleaned_data['config_pretty'])
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON: {e}")

    def save(self, commit=True):
        self.instance.config = self.cleaned_data.get('config_pretty', {})
        return super().save(commit)

# ──────────────── TransformationStepForm ────────────────

STEP_CONFIG_EXAMPLES = {
    "rename_columns": {
        "mapping": {
            "old_column": "new_column"
        }
    },
    "drop_columns": {
        "columns": ["col1", "col2"]
    },
    "explode_column": {
        "column": "tags"
    },
    "filter_rows": {
        "column": "status",
        "condition": "==",
        "value": "active"
    },
    "remove_duplicates": {
        "subset": ["email"],
        "keep": "first"
    },
    "add_columns": {
        "new_column": "total",
        "formula": "df['price'] * df['quantity']"
    }
}

# Examples for different transformations
STEP_CONFIG_EXAMPLES = {
    "rename_columns": {
        "mapping": {
            "old_column": "new_column"
        }
    },
    "drop_columns": {
        "columns": ["col1", "col2"]
    },
    "explode_column": {
        "column": "tags"
    },
    "filter_rows": {
        "column": "status",
        "condition": "==",
        "value": "active"
    },
    "remove_duplicates": {
        "subset": ["email"],
        "keep": "first"
    },
    "add_columns": {
        "new_column": "total",
        "formula": "df['price'] * df['quantity']"
    }
}

class TransformationStepForm(forms.ModelForm):
    config_pretty = forms.CharField(
        label="Configuration (JSON format)",
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 80}),
        help_text="Specify how the transformation should be applied. See example below."
    )

    class Meta:
        model = TransformationStep
        fields = ['preset', 'step_type', 'order']  # config is managed via config_pretty

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fill in config_pretty from the instance config
        if self.instance and self.instance.config:
            self.fields['config_pretty'].initial = json.dumps(self.instance.config, indent=2)

        # Add all examples to the help text
        examples_text = "\n\n".join(
            f"{step_type}:\n{json.dumps(example, indent=2)}"
            for step_type, example in STEP_CONFIG_EXAMPLES.items()
        )
        self.fields['config_pretty'].help_text += (
            f"<br><br><strong>Examples for different step types:</strong><pre>{examples_text}</pre>"
        )

    def clean_config_pretty(self):
        try:
            return json.loads(self.cleaned_data['config_pretty'])
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON: {e}")

    def save(self, commit=True):
        self.instance.config = self.cleaned_data.get('config_pretty', {})
        return super().save(commit)
