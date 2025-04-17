from typing import List, Dict, Optional
from datetime import datetime, timedelta
from call_api import call_api_with_patient_id

def process_patient_data(values: Dict, use_cache: bool = None, from_date: str = None, to_date: str = None) -> List[Dict]:
    """Process API calls for each patient ID and collect data."""
    all_patient_data = []
    
    print("\nProcessing API calls for each patient ID...")
    for acc_no, patient_id in zip(values['acc_no'], values['patientid']):
        print(f"\nFetching data for patient ID: {patient_id}")
        try:
            
            patient_data = call_api_with_patient_id(patient_id, use_cache, from_date, to_date, acc_no)
            
            if patient_data:
                all_patient_data.append(patient_data)
                print(f"Successfully processed patient {patient_id}")
            else:
                print(f"No data returned for patient {patient_id}")
        except Exception as e:
            print(f"Error processing patient {patient_id}: {str(e)}")
    
    return all_patient_data 