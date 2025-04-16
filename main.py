import pandas as pd
import time
from typing import List, Dict, Optional
from call_api import call_api_with_patient_id
from read_csv import read_last_values

def process_patient_data(patient_ids: List[str], use_cache: bool = True) -> List[Dict]:
    """Process API calls for each patient ID and collect data."""
    all_patient_data = []
    
    print("\nProcessing API calls for each patient ID...")
    for patient_id in patient_ids:
        print(f"\nFetching data for patient ID: {patient_id}")
        try:
            patient_data = call_api_with_patient_id(patient_id, use_cache)
            if patient_data:
                all_patient_data.append(patient_data)
                print(f"Successfully processed patient {patient_id}")
            else:
                print(f"No data returned for patient {patient_id}")
        except Exception as e:
            print(f"Error processing patient {patient_id}: {str(e)}")
    
    return all_patient_data

def save_to_excel(data: List[Dict], filename: str = "patient_data.xlsx") -> bool:
    """Save patient data to Excel file."""
    try:
        if not data:
            print("\nNo data to save")
            return False
            
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"\nData saved to {filename}")
        return True
    except Exception as e:
        print(f"\nError saving to Excel: {str(e)}")
        return False

def main():
    try:
        # Read patient IDs from CSV
        csv_file = "Registry_Report_1744325041903.csv"
        patient_ids = read_last_values(csv_file, 10)
        
        if not patient_ids:
            print("\nNo patient IDs found in CSV file")
            return
            
        # Process patient data
        all_patient_data = process_patient_data(patient_ids)
        
        # Save results
        if all_patient_data:
            save_to_excel(all_patient_data)
        else:
            print("\nNo patient data was collected")
            
    except Exception as e:
        print(f"\nUnexpected error in main: {str(e)}")

if __name__ == "__main__":
    main()