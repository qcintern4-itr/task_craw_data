import csv
import pandas as pd
from typing import List, Dict, Optional 
from config import ENCOUNTER_FIELD_MAPPINGS
from processing_api.call_api import call_api_search_patient

def read_last_values(file_path, num_values=1):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            
            values = {'acc_no': [], 'patientid': []}
            for i, row in enumerate(csv_reader):
                if i >= num_values:  
                    break
                if row:  
                    value = row[-1]
                    # Kiểm tra nếu value là số
                    if value.isdigit():                
                        values['acc_no'].append(value)
                        values['patientid'].append(value)
                    else:
                        patient_data = call_api_search_patient(value, False)
                        
                        if patient_data:
                            values['acc_no'].append(value)
                            values['patientid'].append(patient_data['patientid'])
            # Print values
            print("\nPrint values (id-patientid):")
            for key, value in values.items():
                print(f"{key}: {value}")
            
            return values
            
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        


def save_to_excel(data: List[Dict], filename: str = "patient_data.xlsx") -> bool:
    """Save patient data to Excel file with columns ordered according to ENCOUNTER_FIELD_MAPPINGS."""
    try:
        if not data:
            print("\nNo data to save")
            return False
            
        # Tạo DataFrame từ dữ liệu
        df = pd.DataFrame(data)
        
        # Lấy danh sách cột theo thứ tự từ ENCOUNTER_FIELD_MAPPINGS
        ordered_columns = list(ENCOUNTER_FIELD_MAPPINGS.keys())
        
        # Thêm các cột không có trong mapping nhưng có trong dữ liệu
        extra_columns = [col for col in df.columns if col not in ordered_columns]
        ordered_columns.extend(extra_columns)
        
        # Sắp xếp lại các cột theo thứ tự
        df = df[ordered_columns]
        
        # Lưu vào Excel
        df.to_excel(filename, index=False)
        print(f"\nData saved to {filename}")
        return True
    except Exception as e:
        print(f"\nError saving to Excel: {str(e)}")
        return False 
