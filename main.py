import pandas as pd
import time
from call_api import call_api_with_patient_id
from read_csv import read_last_values

def main():
    csv_file = "Registry_Report_1744325041903.csv"
    patient_ids = read_last_values(csv_file, 10)
    
    if patient_ids:
        print("\nProcessing API calls for each patient ID...")
        all_patient_data = []
        
        for patient_id in patient_ids:
            print(f"\nFetching data for patient ID: {patient_id}")
            patient_data = call_api_with_patient_id(patient_id, use_cache=False)
            if patient_data:
                all_patient_data.append(patient_data)
            time.sleep(1) 
        
        # Create DataFrame and save to Excel
        if all_patient_data:
            df = pd.DataFrame(all_patient_data)
            excel_filename = f"patient_data.xlsx"
            df.to_excel(excel_filename, index=False)
            print(f"\nData saved to {excel_filename}")

if __name__ == "__main__":
    main()
    