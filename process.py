from typing import List, Dict, Optional
from call_api import call_api_with_patient_id

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