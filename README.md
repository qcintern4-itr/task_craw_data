# Medical Records Data Crawler

This project crawls medical records data from a clinical web endpoint and saves the results to an Excel file.

## Features

- Reads patient IDs from CSV file
- Makes API calls to fetch patient encounter data
- Saves XML responses to cache files
- Transforms and formats data for Excel output
- Supports caching to avoid unnecessary API calls

## Usage

1. Place your CSV file (Registry_Report_1744325041903.csv) in the project directory
2. Run the script:
   ```bash
   python main.py
   ```

## Configuration

### Number of Records to Crawl

By default, the script crawls 10 patient IDs from the CSV file. To change this number:

1. Open `main.py`
2. Modify the parameter in the `read_last_values()` function call:
   ```python
   # Example: to crawl 20 records
   patient_ids = read_last_values(csv_file, 20)
   ```

### Cache Usage

The script uses caching to store XML responses:
- Cache files are stored in the `container_xml` directory
- Each patient's data is saved as `patient_{id}.xml`
- To force fresh API calls, set `use_cache=False` in `call_api_with_patient_id()`. If have cache then set `use_cache=True`

## Output

- Excel file: `patient_data.xlsx`
- XML cache files: `container_xml/patient_{id}.xml`

## Data Transformation

The script performs the following transformations:
- Date format: YYYY-MM-DD → DD/MM/YYYY
- Chart lock status: 1 → "Locked", 0 → "Unlocked"
- Unbilled status: 1 → "FALSE", 0 → "TRUE" 