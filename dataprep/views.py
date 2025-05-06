import pandas as pd
import requests
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import DataPreset
from .utils.data_import import extract_flat_dataframe

"""
views.py – Core view logic for executing data transformation workflows via user-defined presets.

This module handles the following key responsibilities:

1. run_preset(request, slug)
   - Retrieves a DataPreset based on the URL slug.
   - Loads data from an associated DataSource (currently supports APIs).
   - Supports dynamic configuration of:
       - API URL and method
       - Optional root_key for extracting the main data list
       - Optional record_path and meta_fields for flattening nested lists using pandas.json_normalize
   - Automatically flattens the data into a pandas DataFrame.
   - Applies a sequence of TransformationStep operations on the DataFrame, such as:
       - Renaming columns
       - Dropping columns
       - Exploding list columns
       - (Support for more step types can be added here)
   - Returns the transformed data as a JSON response.

The goal of this view is to enable dynamic, reusable, and declarative data processing workflows,
where end-users configure everything through the admin interface or UI – without writing code.

This file separates runtime logic (data loading + transformation) from configuration (defined in models),
and serves as the execution engine for any saved preset.
"""


def run_preset(request, slug):

    """
    Executes a user-defined data processing pipeline based on a saved DataPreset.

    Steps performed:
    1. Retrieves the DataPreset object using the provided slug.
    2. Loads data from the associated DataSource (currently supports APIs via HTTP requests).
    3. Optionally extracts a list from the response using `root_key`, and flattens nested structures using
       `record_path` and `meta_fields` if provided in the DataSource config (Admin UI).
    4. Converts the loaded data into a pandas DataFrame.
    5. Applies each TransformationStep linked to the preset, in defined order. Supported step types include:
        - rename_columns: Renames columns using a mapping
        - drop_columns: Removes specified columns
        - explode_column: Expands a list column into multiple rows
        (At the time of writing 2025-05-06: More step types will be written into the final valid code and can be added dynamically via the admin interface)
    6. Returns the final transformed DataFrame as a JSON response (list of records).

    Parameters:
        request: The Django HTTP request (GET or POST).
        slug (str): The slug identifier for the DataPreset to execute.

    Returns:
        JsonResponse: Transformed data serialized as a list of JSON records.

    Notes:
        - All behavior is controlled by configuration stored in the database.
        - This function is intended to support repeatable, no-code data workflows.
    """

    preset = get_object_or_404(DataPreset, slug=slug)
    source = preset.source

    if source.source_type == "api":
        config = source.config
        url = config.get("url")
        method = config.get("method", "GET").upper()
        headers = config.get("headers", {})
        params = config.get("params", {})
        root_key = config.get("root_key")
        record_path = config.get("record_path")
        meta_fields = config.get("meta_fields")

        try:
            response = requests.request(method, url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

        df = extract_flat_dataframe(data, root_key, record_path, meta_fields)

        for step in preset.steps.order_by("order"):
            cfg = step.config
            if step.step_type == "rename_columns":
                df.rename(columns=cfg.get("mapping", {}), inplace=True)
            elif step.step_type == "drop_columns":
                df.drop(columns=cfg.get("columns", []), inplace=True, errors="ignore")
            elif step.step_type == "explode_column":
                col = cfg.get("column")
                if col in df.columns:
                    df = df.explode(col)

        return JsonResponse(df.to_dict(orient="records"), safe=False)

    return JsonResponse({"error": "Unsupported source type"}, status=400)
