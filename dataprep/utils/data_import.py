import pandas as pd

def extract_flat_dataframe(data, root_key=None, record_path=None, meta_fields=None):
    """
Returns a flattened DataFrame from a JSON API response.

API example - https://dummyjson.com/carts

- root_key: str (optional) → e.g. 'carts'
- record_path: str or list (optional) → for nested objects, e.g. 'products'
- meta_fields: list (optional) → e.g. ['userId']

Uses pandas.json_normalize() to create a flattened structure.
    """
    if root_key and isinstance(data, dict):
        data = data.get(root_key, [])

    if isinstance(record_path, str):
        record_path = [record_path]

    if record_path:
        return pd.json_normalize(
            data,
            record_path=record_path,
            meta=meta_fields,
            sep="__"
        )
    else:
        return pd.json_normalize(data, sep="__") if isinstance(data, (list, dict)) else pd.DataFrame()
