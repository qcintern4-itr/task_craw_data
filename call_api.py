import requests
from read_csv import read_last_values
import time
import xml.etree.ElementTree as ET
from config import (
    API_URL_TABLE2, API_PARAMS_TABLE2, API_HEADERS_TABLE2,
    API_URL_TABLE3, API_PARAMS_TABLE3, API_HEADERS_TABLE3
)
from cache import (
    save_xml_response_table2, save_xml_response_table3,
    load_xml_response_table2, load_xml_response_table3
)
from extract import extract_xml_values_table2, extract_xml_values_table3

def call_api_with_patient_id(patient_id, use_cache):
    if use_cache:
        cached_response = load_xml_response_table2(patient_id)
        if cached_response:
            print(f"Using cached data for patient {patient_id}")
            patient_data = extract_xml_values_table2(cached_response)
            if patient_data:
                patient_data['patientid'] = patient_id
                # Lấy encounterID từ XML
                try:
                    root = ET.fromstring(cached_response)
                    encounter_element = root.find('.//encounterID')
                    if encounter_element is not None:
                        encounter_id = encounter_element.text
                        # Gọi API để lấy createdate
                        encounter_data = call_api_with_encounter_id(encounter_id, True)
                        if encounter_data and 'createdate' in encounter_data:
                            patient_data['createdate'] = encounter_data['createdate']
                except ET.ParseError:
                    pass
                print(patient_data)
            return patient_data

    params = API_PARAMS_TABLE2.copy()
    params.update({
        "PatientId": patient_id,
    })

    try:
        response = requests.get(API_URL_TABLE2, headers=API_HEADERS_TABLE2, params=params)
        
        if response.status_code == 200:
            save_xml_response_table2(patient_id, response.text)
            patient_data = extract_xml_values_table2(response.text)
            if patient_data:
                patient_data['patientid'] = patient_id
                # Lấy encounterID từ XML
                try:
                    root = ET.fromstring(response.text)
                    encounter_element = root.find('.//encounterID')
                    if encounter_element is not None:
                        encounter_id = encounter_element.text
                        # Gọi API để lấy createdate
                        encounter_data = call_api_with_encounter_id(encounter_id, False)
                        if encounter_data and 'createdate' in encounter_data:
                            patient_data['createdate'] = encounter_data['createdate']
                except ET.ParseError:
                    pass
                print(patient_data)
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
        response = requests.get(API_URL_TABLE3, headers=API_HEADERS_TABLE3, params=params)
        
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

