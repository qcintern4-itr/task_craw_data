# Medical Records Data Crawler

A robust tool for automating medical records data processing and web interactions with eClinicalWorks.

## Features

- Automated data crawling from eClinicalWorks
- Multiple API endpoint support (TABLE2, TABLE3, TABLE6)
- Intelligent caching system
- Data transformation and formatting
- Comprehensive error handling and logging
- Excel output generation

## Project Structure

```
.
├── main.py              # Main script entry point
├── config.py            # API and configuration settings
├── call_api.py          # API call handling
├── extract.py           # Data extraction utilities
├── transform.py         # Data transformation functions
├── cache.py            # Caching system
├── read_csv.py         # CSV file handling
├── patient_data.xlsx   # Output Excel file
└── container_*/        # Cache directories
```

## Installation

1. Clone the repository

## Usage

1. Place your CSV file in the project directory
2. Run the script:
```bash
python main.py
```

## Configuration

### API Configuration (`config.py`)
- Base URLs and endpoints
- Common request parameters
- Headers configuration
- Field mappings

### Cache Configuration
Cache files are organized in separate directories:
- `container_xml_table2/`: Patient encounter data
- `container_xml_table3/`: Encounter logs
- `container_json_table6/`: Lab data


## Data Processing

### API Endpoints
1. TABLE2: Patient encounter data
2. TABLE3: Encounter logs
3. TABLE6: Lab data

### Data Transformation
- Date formats: YYYY-MM-DD → DD/MM/YYYY
- Status codes:
  - Chart lock: 1 → "Locked", 0 → "Unlocked"
  - Billing status: 1 → "FALSE", 0 → "TRUE"
- ICD codes: Combined into comma-separated string
- NPI: Converted to string format

## Error Handling

The system includes comprehensive error handling:
- API request failures
- Data parsing errors
- File I/O issues
- Cache management
- Rate limiting

## Output

### Data Files
- Excel file: `patient_data.xlsx`
- Cache files in respective directories

## Note
Format JSON files using: `Shift + Alt + F`