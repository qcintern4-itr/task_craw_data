import requests
import json
from typing import Dict, Optional, Any
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

def _make_request(url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
    """Make HTTP request with error handling."""
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None

def _handle_response(response: requests.Response, cache_func: callable, 
                    extract_func: callable, cache_id: str) -> Optional[Dict]:
    """Handle API response and cache if successful."""
    if response.status_code == 200:
        cache_func(cache_id, response.text)
        return extract_func(response.text)
    print(f"API returned status code: {response.status_code}")
    return None

def call_api_with_patient_id(patient_id: str, use_cache: bool = True) -> Optional[Dict]:
    """Fetch patient data and related information."""
    if use_cache:
        cached_response = load_xml_response_table2(patient_id)
        if cached_response:
            print(f"Using cached data for patient {patient_id}")
            patient_data = extract_xml_values_table2(cached_response)
            if patient_data:
                return _enrich_patient_data(patient_data, patient_id, use_cache)
            return None

    params = {**API_PARAMS_TABLE2, "PatientId": patient_id}
    response = _make_request(API_URL_TABLE2, params=params, headers=API_HEADERS)
    
    if response:
        patient_data = _handle_response(
            response, save_xml_response_table2, 
            extract_xml_values_table2, patient_id
        )
        if patient_data:
            return _enrich_patient_data(patient_data, patient_id, use_cache)
    return None

def _enrich_patient_data(patient_data: Dict, patient_id: str, use_cache: bool) -> Dict:
    """Enrich patient data with additional information."""
    patient_data['patientid'] = patient_id
    patient_data['isdeleted'] = 'FALSE'
    
    # Get lab data
    table6_data = call_api_table6(use_cache, patient_data)
    if table6_data:
        patient_data.update({
            'npi': table6_data.get('npi', ''),
            'icd_code_10': table6_data.get('icd_code_10', '')
        })
    
    # Get encounter data
    encounter_data = call_api_with_encounter_id(patient_data['id'], use_cache)
    if encounter_data and 'createdate' in encounter_data:
        patient_data['createdate'] = encounter_data['createdate']
    
    return patient_data

def call_api_with_encounter_id(encounter_id: str, use_cache: bool = True) -> Optional[Dict]:
    """Fetch encounter data."""
    if use_cache:
        cached_response = load_xml_response_table3(encounter_id)
        if cached_response:
            print(f"Using cached data for encounter {encounter_id}")
            return extract_xml_values_table3(cached_response)

    params = {**API_PARAMS_TABLE3, "EncounterId": encounter_id}
    response = _make_request(API_URL_TABLE3, params=params, headers=API_HEADERS)
    
    if response:
        return _handle_response(
            response, save_xml_response_table3,
            extract_xml_values_table3, encounter_id
        )
    return None

def call_api_table6(use_cache: bool, patient_data: Dict) -> Optional[Dict]:
    """Fetch lab data for patient."""
    if use_cache:
        cached_response = load_json_response_table6(patient_data['id'])
        if cached_response:
            print(f"Using cached lab data for patient {patient_data['id']}")
            return extract_json_values_table6(cached_response)

    # Prepare request data
    quick_search_filter = {**QuickSearchFilterObj, **{
        "nPatientId": patient_data['patientid'],
        "nEncounterId": patient_data['id'],
        "nDoctorId": patient_data['physicianid']
    }}
    
    form_data = {
        **FORM_DATA_TABLE6,
        "QuickSearchFilterObj": json.dumps(quick_search_filter)
    }
    
    headers = {
        **API_HEADERS,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    
    response = _make_request(
        API_URL_TABLE6,
        method='POST',
        headers=headers,
        params=API_PARAMS_TABLE6,
        data=form_data
    )
    
    if response:
        try:
            response_data = response.json()
            save_json_response_table6(patient_data['id'], response_data)
            return extract_json_values_table6(json.dumps(response_data))
        except ValueError as e:
            print(f"Error parsing JSON response: {str(e)}")
    return None

