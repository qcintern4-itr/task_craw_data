# Medical Records Data Crawler

A robust tool for automating medical records data processing and web interactions with eClinicalWorks.

## Features

- Automated data crawling from eClinicalWorks
- Multiple API endpoint support (DETAIL_ENCOUNTER, DETAIL_LOG, DELETE_ENCOUNTER, DETAIL_LAB, PATIENT_SEARCH)
- Intelligent caching system
- Data transformation and formatting
- Comprehensive error handling
- Excel output generation

## Project Structure

```
.
├── main.py                    # Main script entry point
├── config.py                  # API and configuration settings
├── processing_api/            # Processing crawl api 
|   ├──call_api.py             # API call handling
|   ├── extract.py             # Data extraction utilities
|   ├── transform.py           # Data transformation functions
|   └── cache.py               # Caching system
├── handle_file/               # Processing call methods and handle file input & output
|   ├── process.py             # API call handling
|   └── implement_file.py      # File handling and output generation
├── input/                     # Input directory for CSV files
|   └── input.csv/             # Input files csv
├── results/                   # Output directory
│   └── output_file_YYYYMMDD/  # Output files with timestamp
└── cache/                     # Cache directories

```

## Installation

1. Clone the repository
2. Create an `input` folder in the project directory
3. Place your CSV file in the `input` folder

## Usage

1. Prepare your input file:
   - Create an `input` folder in the project directory
   - Place your CSV file (e.g., `Registry_Report_1744325041903.csv`) in the `input` folder

2. Run the script with parameters:
```bash
python main.py -f Registry_Report_1744325041903.csv -n 10 -o output.xlsx -uc true --from-date 1/4/2025 --to-date 1/4/2025
```

### Command Line Arguments
- `-f, --file`: Input CSV file name (required)
- `-n, --number`: Number of records to process (optional, default: 10)
- `-o, --output`: Output Excel file name (optional, default: output.xlsx)
- `-uc, --use-cache`: Use cached data (true/false) (optional, default: true)
- `--from-date`: Start date in MM/DD/YYYY format (optional)
- `--to-date`: End date in MM/DD/YYYY format (optional)

### Examples
```bash
# Process 10 records from Registry_Report_1744325041903.csv
python main.py -f Registry_Report_1744325041903.csv -n 10 -o output.xlsx -uc true --from-date 1/4/2025 --to-date 1/4/2025

# Process all records from Registry_Report_1744325041903.csv
python main.py -f Registry_Report_1744325041903.csv -o output.xlsx -uc true --from-date 1/4/2025 --to-date 1/4/2025
```

## Configuration

### API Configuration (`config.py`)
- Base URLs and endpoints
- Common request parameters
- Headers configuration
- Field mappings
- Form data templates

### Cache Configuration
Cache files are organized in separate directories:
```
├──cache
  ├──detail_encounter_{id}      # Patient encounter data
  ├── detail_log_{id}            # Encounter logs
  ├── detail_lab_{id}            # Lab data
```

## Data Processing

### API Endpoints
1. DETAIL_ENCOUNTER: Patient encounter data
2. DETAIL_LOG: Encounter logs
3. DELETE_ENCOUNTER: Encounter deletion
4. DETAIL_LAB: Lab data
5. PATIENT_SEARCH: Patient search by account number

### Data Transformation
- Date formats: YYYY-MM-DD → DD/MM/YYYY
- Status codes:
  - Chart lock: 1 → "Locked", 0 → "Unlocked"
  - Billing status: 1 → "FALSE", 0 → "TRUE"
- ICD codes: Combined into comma-separated string
- NPI: Converted to string format

## Output

### Data Files
- Excel file: `results/output_file_YYYYMMDD/output.xlsx`
- Cache files in respective directories

## Note
Format JSON files using: `Shift + Alt + F`