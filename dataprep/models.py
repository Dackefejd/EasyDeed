from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import SET

# Returns the default user 'Eddy' which is used as a fallback if the original user (e.g. the creator of a DataPreset) has been deleted. Eddy represents the EasyDeed default user.
def get_eddy_user():
    return get_user_model().objects.get(username='Eddy')

# SOURCE_TYPE - Users choose whether the data preset should be for retrieving data via REST API or whether it should be loaded as a CSV/XLSX
class DataSource(models.Model):
    SOURCE_TYPE = [
        ("file", "CSV/XLSX File"),
        ("api", "API")
    ]

    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=SET(get_eddy_user), null=True, blank=True)
    source_type = models.CharField(max_length=30, choices=SOURCE_TYPE)
    config = models.JSONField("API or file settings. The structure varies depending on the type.")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.name} ({self.source_type})'



class DataPreset(models.Model):
    user = models.ForeignKey(User, on_delete=SET(get_eddy_user), null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name} Owner: {self.user} | Created: {self.created.strftime("%Y-%m-%d")} | Updated: {self.updated.strftime("%Y-%m-%d")}'


# STEP_TYPES - List of available transformation types.
# These are used to identify the type of operation to be applied to the data.
# Each tuple contains an internal value (stored in the database) and a human-readable label (displayed in e.g. the admin panel).
# The list can be extended with more types as needed, e.g. "custom_formula", "sort_rows", etc. 

STEP_TYPES = [
    ("drop_columns", "Drop Columns"),
    ("filter_rows", "Filter Rows"),
    ("reorder_columns", "Reorder Columns"),
    ("rename_columns", "Rename Columns"),
    ("remove_duplicates", "Remove Duplicates"),
    ("add_columns", "Add Columns"),
]

class TransformationStep(models.Model):
    preset = models.ForeignKey(DataPreset, related_name='steps', on_delete=models.CASCADE)
    step_type = models.CharField(max_length=100, choices=STEP_TYPES)
    config = models.JSONField() # JSON-based configuration specifying how the transformation should be applied. Example for 'drop_columns': {"columns": ["A", "B"]}
    order = models.PositiveIntegerField() # Used to define the order in which the transformation steps should be applied

    def __str__(self):
        return f'{self.order}: {self.step_type} in "{self.preset.name}"'