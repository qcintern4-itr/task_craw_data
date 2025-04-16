import csv
import pandas as pd
from typing import List, Dict, Optional 

def read_last_values(file_path, num_values=1):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            
            values = []
            for i, row in enumerate(csv_reader):
                if i >= num_values:  
                    break
                if row:  
                    values.append(row[-1])  
            
            # Print values
            print("\nPrint values (id-patientid):")
            for value in values:
                print(value)
            
            return values
            
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        


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
