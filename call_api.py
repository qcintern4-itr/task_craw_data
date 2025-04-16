import requests
from read_csv import read_last_values
import time
import xml.etree.ElementTree as ET
import json
from config import (
    API_URL_TABLE2, API_PARAMS_TABLE2, API_HEADERS,
    API_URL_TABLE3, API_PARAMS_TABLE3,
    API_URL_TABLE6, API_PARAMS_TABLE6, FORM_DATA_TABLE6,
    QuickSearchFilterObj
)
from cache import (
    save_xml_response_table2, save_xml_response_table3, 
    load_xml_response_table2, load_xml_response_table3, 
    save_json_response_table6, load_json_response_table6,
)
from extract import (
    extract_xml_values_table2, extract_xml_values_table3, 
    extract_json_values_table6,
)

def call_api_with_patient_id(patient_id, use_cache):
    if use_cache:
        cached_response = load_xml_response_table2(patient_id)
        if cached_response:
            print(f"Using cached data for patient {patient_id}")
            patient_data = extract_xml_values_table2(cached_response)
            if patient_data:
                patient_data['patientid'] = patient_id
                patient_data['isdeleted'] = 'FALSE'
                
                table6_data = call_api_table6(True, patient_data)
                patient_data['npi'] = table6_data['npi']
                patient_data['icd_code_10'] = table6_data['icd_code_10']
                # Gọi API để lấy createdate
                encounter_data = call_api_with_encounter_id(patient_data['id'], True)
                if encounter_data and 'createdate' in encounter_data:
                    patient_data['createdate'] = encounter_data['createdate']
            return patient_data

    params = API_PARAMS_TABLE2.copy()
    params.update({
        "PatientId": patient_id,
    })

    try:
        response = requests.get(API_URL_TABLE2, headers=API_HEADERS, params=params)
        
        if response.status_code == 200:
            save_xml_response_table2(patient_id, response.text)
            patient_data = extract_xml_values_table2(response.text)
            if patient_data:
                patient_data['patientid'] = patient_id
                
                table6_data = call_api_table6(False, patient_data)
                patient_data['npi'] = table6_data['npi']
                patient_data['icd_code_10'] = table6_data['icd_code_10']             
                # Gọi API để lấy createdate
                encounter_data = call_api_with_encounter_id(patient_data['id'], False)
                if encounter_data and 'createdate' in encounter_data:
                    patient_data['createdate'] = encounter_data['createdate']
                # print(patient_data)
            return patient_data
        else:
            print(f"Failed to fetch data for patient {patient_id}: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error occurred for patient {patient_id}: {str(e)}")
        return None

def call_api_with_encounter_id(encounter_id, use_cache):
    if use_cache:
        cached_response = load_xml_response_table3(encounter_id)
        if cached_response:
            print(f"Using cached data for encounter {encounter_id}")
            encounter_data = extract_xml_values_table3(cached_response)
            return encounter_data

    params = API_PARAMS_TABLE3.copy()
    params.update({
        "EncounterId": encounter_id,
    })

    try:
        response = requests.get(API_URL_TABLE3, headers=API_HEADERS, params=params)
        
        if response.status_code == 200:
            save_xml_response_table3(encounter_id, response.text)
            encounter_data = extract_xml_values_table3(response.text)
            return encounter_data
        else:
            print(f"Failed to fetch data for encounter {encounter_id}: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error occurred for encounter {encounter_id}: {str(e)}")
        return None

def call_api_table6(use_cache, patient_data=None):
    quick_search_filter = QuickSearchFilterObj.copy()
    quick_search_filter.update({
        "nPatientId": patient_data['patientid'],
        "nEncounterId": patient_data['id'],
        "nDoctorId": patient_data['physicianid']
    })
    form_data = FORM_DATA_TABLE6.copy()
    form_data["QuickSearchFilterObj"] = json.dumps(quick_search_filter)
    
    headers = API_HEADERS.copy()
    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    
    if use_cache:
        cached_response = load_json_response_table6(patient_data['id'])
        if cached_response:
            labs_data = extract_json_values_table6(cached_response)
            return labs_data
        return None

    try:
        response = requests.post(
            API_URL_TABLE6, 
            headers=headers, 
            params=API_PARAMS_TABLE6,
            data=form_data
        )
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                save_json_response_table6(patient_data['id'], json.dumps(response_data))
                labs_data = extract_json_values_table6(json.dumps(response_data))
                return labs_data
            except ValueError as e:
                print("Error parsing JSON response:", e)
                return None
        else:
            return None
            
    except Exception as e:
        print(f"Error occurred while fetching labs data: {str(e)}")
        return None

