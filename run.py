import pandas as pd
import time
import logging
from typing import List, Dict, Optional
from call_api import call_api_with_patient_id
from implement_file import read_last_values

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

def process_patient_data(patient_ids: List[str], use_cache: bool = True) -> List[Dict]:
    """Process API calls for each patient ID and collect data."""
    all_patient_data = []
    
    for patient_id in patient_ids:
        logging.info(f"Processing patient ID: {patient_id}")
        try:
            patient_data = call_api_with_patient_id(patient_id, use_cache)
            if patient_data:
                all_patient_data.append(patient_data)
                logging.info(f"Successfully processed patient {patient_id}")
            else:
                logging.warning(f"No data returned for patient {patient_id}")
        except Exception as e:
            logging.error(f"Error processing patient {patient_id}: {str(e)}")
        
        time.sleep(1)  # Rate limiting
    
    return all_patient_data

def save_to_excel(data: List[Dict], filename: str = "patient_data.xlsx") -> bool:
    """Save patient data to Excel file."""
    try:
        if not data:
            logging.warning("No data to save")
            return False
            
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        logging.info(f"Data saved to {filename}")
        return True
    except Exception as e:
        logging.error(f"Error saving to Excel: {str(e)}")
        return False

def main():
    try:
        # Read patient IDs from CSV
        csv_file = "Registry_Report_1744325041903.csv"
        patient_ids = read_last_values(csv_file, 10)
        
        if not patient_ids:
            logging.error("No patient IDs found in CSV file")
            return
            
        # Process patient data
        all_patient_data = process_patient_data(patient_ids)
        
        # Save results
        if all_patient_data:
            save_to_excel(all_patient_data)
        else:
            logging.warning("No patient data was collected")
            
    except Exception as e:
        logging.error(f"Unexpected error in main: {str(e)}")

if __name__ == "__main__":
    main() 