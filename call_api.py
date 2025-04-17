import requests
import json
from typing import Dict, Optional, Any
from config import (
    API_URL_DETAIL_ENCOUNTER, API_PARAMS_DETAIL_ENCOUNTER, API_HEADERS,
    API_URL_DETAIL_LOG, API_PARAMS_DETAIL_LOG,
    API_URL_DELETE_ENCOUNTER, API_PARAMS_DELETE_ENCOUNTER,
    API_URL_DETAIL_LAB, API_PARAMS_DETAIL_LAB, FORM_DATA_DETAIL_LAB,
    API_URL_PATIENT_SEARCH, API_PARAMS_PATIENT_SEARCH, FORM_DATA_PATIENT_SEARCH,
    QuickSearchFilterObj
)
from cache import (
    save_xml_response_detail_encounter, save_xml_response_detail_log, 
    load_xml_response_detail_encounter, load_xml_response_detail_log, 
    save_json_response_detail_lab, load_json_response_detail_lab, 
    save_xml_response_search_patient, load_xml_response_search_patient,
)
from extract import (
    extract_xml_values_detail_encounter, extract_xml_values_detail_log, 
    extract_json_values_detail_lab, extract_xml_values_search_patient
    
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

def call_api_with_patient_id(patient_id: str, use_cache: bool, from_date: str = None, to_date: str = None, acc_no: str = None) -> Optional[Dict]:
    """Fetch patient data and related information."""
    if use_cache:
        cached_response = load_xml_response_detail_encounter(patient_id)
        if cached_response:
            print(f"Using cached data for patient {patient_id}")
            patient_data = extract_xml_values_detail_encounter(cached_response)
            if patient_data:
                return _enrich_patient_data(patient_data, patient_id, use_cache, from_date, to_date, acc_no)
            return None

    params = {**API_PARAMS_DETAIL_ENCOUNTER, "PatientId": patient_id, "fromDate": from_date, "toDate": to_date}
    response = _make_request(API_URL_DETAIL_ENCOUNTER, params=params, headers=API_HEADERS)
    if response:
        patient_data = _handle_response(
            response, save_xml_response_detail_encounter, 
            extract_xml_values_detail_encounter, patient_id
        )
        if patient_data:
            return _enrich_patient_data(patient_data, patient_id, use_cache, from_date, to_date, acc_no)
    return None

def _enrich_patient_data(patient_data: Dict, patient_id: str, use_cache: bool, from_date: str = None, to_date: str = None, acc_no: str = None) -> Dict:
    """Enrich patient data with additional information."""
    patient_data['patientid'] = patient_id
    patient_data['acc_no'] = acc_no
    patient_data['isdeleted'] = 'FALSE'
    
    # Get lab data
    detail_lab_data = call_api_detail_lab(use_cache, patient_data, from_date, to_date)
    
    if detail_lab_data:
        patient_data.update({
            'npi': detail_lab_data.get('npi', ''),
            'icd_code_10': detail_lab_data.get('icd_code_10', '')
        })
    
    # Get encounter data
    encounter_data = call_api_with_encounter_id(patient_data['id'], use_cache, from_date, to_date)
    if encounter_data and 'createdate' in encounter_data:
        patient_data['createdate'] = encounter_data['createdate']
    
    
    return patient_data

def call_api_with_encounter_id(encounter_id: str, use_cache: bool, from_date: str = None, to_date: str = None) -> Optional[Dict]:
    """Fetch encounter data."""
    if use_cache:
        cached_response = load_xml_response_detail_log(encounter_id)
        if cached_response:
            print(f"Using cached data for encounter {encounter_id}")
            return extract_xml_values_detail_log(cached_response)

    params = {**API_PARAMS_DETAIL_LOG, "EncounterId": encounter_id, "fromDate": from_date, "toDate": to_date}
    response = _make_request(API_URL_DETAIL_LOG, params=params, headers=API_HEADERS)
    
    if response:
        return _handle_response(
            response, save_xml_response_detail_log,
            extract_xml_values_detail_log, encounter_id
        )
    return None

def call_api_detail_lab(use_cache: bool, patient_data: Dict, from_date: str = None, to_date: str = None) -> Optional[Dict]:
    """Fetch lab data for patient."""
    if use_cache:
        cached_response = load_json_response_detail_lab(patient_data['id'])
        if cached_response:
            print(f"Using cached lab data for patient {patient_data['id']}")
            return extract_json_values_detail_lab(cached_response)

    # Prepare request data
    quick_search_filter = {**QuickSearchFilterObj, **{
        "nPatientId": patient_data['patientid'],
        "nEncounterId": patient_data['id'],
        "nDoctorId": patient_data['physicianid']
    }}
    
    form_data = {
        **FORM_DATA_DETAIL_LAB,
        "QuickSearchFilterObj": json.dumps(quick_search_filter)
    }
    
    headers = {
        **API_HEADERS,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    
    params = {**API_PARAMS_DETAIL_LAB, "fromDate": from_date, "toDate": to_date}
    
    response = _make_request(
        API_URL_DETAIL_LAB,
        method='POST',
        headers=headers,
        params=params,
        data=form_data
    )
    
    if response:
        try:
            response_data = response.json()
            save_json_response_detail_lab(patient_data['id'], response_data)
            
            return extract_json_values_detail_lab(json.dumps(response_data))
        except ValueError as e:
            print(f"Error parsing JSON response: {str(e)}")
    return None

def call_api_search_patient(acc_no: str, use_cache: bool) -> Optional[Dict]:
    """Fetch patient id from acc no."""
    if use_cache:
        cached_response = load_xml_response_search_patient(acc_no)
        if cached_response:
            print(f"Using cached data for acc no {acc_no}")
            return extract_xml_values_search_patient(cached_response)

    form_data = {
        **FORM_DATA_PATIENT_SEARCH,
        "AccountNo": acc_no,
        "primarySearchValue": acc_no,
    }
    
    response = _make_request(API_URL_PATIENT_SEARCH, method='POST', params=API_URL_PATIENT_SEARCH, headers=API_HEADERS, data=form_data)
    
    if response:
        return _handle_response(
            response, save_xml_response_search_patient,
            extract_xml_values_search_patient, acc_no
        )
    return None