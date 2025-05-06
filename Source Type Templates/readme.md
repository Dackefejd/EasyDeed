Data Preset Templates
This repository contains JSON templates used as starting points when creating new Data Presets in the EasyDeeds platform. These templates help streamline and standardize the process of retrieving and interpreting data from external sources.

1. API Request Template
json
Kopiera
Redigera
{
  "url": "https://api.example.com/data",
  "method": "GET",
  "headers": {
    "Authorization": "Bearer abc123"
  },
  "params": {
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
  }
}
This template defines how an API request should be configured. It includes:

url: The endpoint of the external data source

method: HTTP method to use (GET, POST, etc.)

headers: Authentication credentials or other necessary headers

params: Query parameters such as date ranges or filters

Used as a base when setting up presets for data retrieval from APIs.

2. CSV Parsing Template
json
Kopiera
Redigera
{
  "expected_columns": ["Name", "Amount", "Date"],
  "delimiter": ","
}
This template is used to define the structure of incoming CSV files. It includes:

expected_columns: The columns that must be present for the file to be considered valid

delimiter: The character used to separate values (e.g., comma, semicolon)

This ensures proper import and validation of CSV files during preset creation.

Usage
When creating a new Data Preset via the admin interface or code, these templates can be used as pre-filled values. They provide a consistent structure and help prevent misconfiguration when setting up data sources.