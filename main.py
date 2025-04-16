from implement_file import read_last_values, save_to_excel
from process import process_patient_data

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