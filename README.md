# Medical Records Data Crawler

This project provides tools for automating medical records data processing and web interactions with eClinicalWorks.

## Project Structure

### Core Files
- `main.py`: Main script to run the data crawling process
- `config.py`: Configuration settings for API endpoints and parameters
- `call_api.py`: Functions for making API calls and handling responses
- `extract.py`: Functions for extracting data from XML/JSON responses
- `transform.py`: Functions for transforming and formatting data
- `cache.py`: Functions for caching API responses
- `read_csv.py`: Functions for reading patient IDs from CSV files

## Features

### Data Crawling
- Reads patient IDs from CSV file
- Makes API calls to fetch patient encounter data
- Supports multiple API endpoints 
- Saves responses to cache files
- Transforms and formats data for Excel output
- Supports caching to avoid unnecessary API calls

## Usage

### Data Crawling
1. Place your CSV file in the project directory
2. Run the script:
```bash
python main.py
```

## Configuration

### API Configuration
The `config.py` file contains:
- API URLs for different endpoints
- Common parameters for API requests
- Headers configuration
- XML field mappings

### Cache Configuration
- Cache files are stored in separate directories:
  - `container_xml_table2/`: Patient encounter data
  - `container_xml_table3/`: Encounter logs
  - `container_xml_table6/`: Lab data
- Each data type is saved with appropriate naming:
  - Patient data: `patient_{id}.xml`
  - Encounter data: `encounter_{id}.xml`
  - Lab data: `labs_{id}.json`

### Cache Usage
- To use cached data: Set `use_cache=True` in API calls
- To force fresh API calls: Set `use_cache=False`

## Data Transformation

The script performs the following transformations:
- Date format: YYYY-MM-DD → DD/MM/YYYY
- Chart lock status: 1 → "Locked", 0 → "Unlocked"
- Unbilled status: 1 → "FALSE", 0 → "TRUE"
- ICD codes: Combined into comma-separated string
- NPI: Converted to string format

## Output

### Data Files
- Excel file: `patient_data.xlsx`
- Cache files in respective directories:
  - `container_xml_table2/`
  - `container_xml_table3/`
  - `container_xml_table6/`

## Note
Format JSON files using: `Shift + Alt + F`