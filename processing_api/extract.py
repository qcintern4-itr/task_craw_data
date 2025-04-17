import xml.etree.ElementTree as ET
import json
from typing import Dict, Optional, Union
from processing_api.transform import transform_value
from config import ENCOUNTER_FIELD_MAPPINGS

def _parse_xml(xml_text: str) -> Optional[ET.Element]:
    """Parse XML text and return root element."""
    try:
        return ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"XML parsing error: {str(e)}")
        return None

def _parse_json(json_text: str) -> Optional[Dict]:
    """Parse JSON text and return dictionary."""
    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {str(e)}")
        return None

def extract_xml_values_detail_encounter(xml_text: str) -> Optional[Dict]:
    """Extract values from XML response for TABLE2 (DETAIL_ENCOUNTER)."""
    try:
        root = ET.fromstring(xml_text)
        patient_data = {}
       
        for field, xml_field in ENCOUNTER_FIELD_MAPPINGS.items():
            element = root.find(f".//{xml_field}")
            
            value = element.text if element is not None else ""
            patient_data[field] = transform_value(field, value)
        
        return patient_data
    except ET.ParseError as e:
        print(f"Error parsing XML for DETAIL_ENCOUNTER: {str(e)}")
        return None

def extract_encounter_id_from_detail_encounter(xml_text: str) -> Optional[str]:
    """Extract encounter ID from DETAIL_ENCOUNTER XML response."""
    root = _parse_xml(xml_text)
    if not root:
        return None

    encounter_element = root.find('.//encounterID')
    return encounter_element.text if encounter_element is not None else None

def extract_xml_values_detail_log(xml_text: str) -> Optional[Dict]:
    """Extract values from XML response for DETAIL_LOG."""
    try:
        root = ET.fromstring(xml_text)
        log_data = {}
        
        for field, xml_field in ENCOUNTER_FIELD_MAPPINGS.items():
            element = root.find(f".//{xml_field}")
            value = element.text if element is not None else ""
            log_data[field] = transform_value(field, value)
        
        return log_data
    except ET.ParseError as e:
        print(f"Error parsing XML for DETAIL_LOG: {str(e)}")
        return None

def extract_json_values_detail_lab(json_text: str) -> Optional[Dict]:
    """Extract values from TABLE6 JSON response."""
    try:
        if isinstance(json_text, str):
            response_data = json.loads(json_text)
        else:
            response_data = json_text

        labs_data = {}
        
        # Get npi from nProviderId
        if 'nProviderId' in response_data:
            labs_data['npi'] = response_data['nProviderId']
        
        # Get icd_code_10 from DxList
        if 'DxList' in response_data and 'Dx' in response_data['DxList']:
            dx_codes = [dx['dxItemCode'] for dx in response_data['DxList']['Dx']]
            labs_data['icd_code_10'] = ', '.join(dx_codes)
        
        return labs_data
    except Exception as e:
        print(f"Error extracting JSON values: {str(e)}")
        return None
    
def extract_xml_values_search_patient(xml_text: str) -> Optional[Dict]:
    """Extract values from XML response for SEARCH_PATIENT."""
    try:
        root = ET.fromstring(xml_text)
        patient_data = {}
        
        for field, xml_field in ENCOUNTER_FIELD_MAPPINGS.items():
            element = root.find(f".//{xml_field}")
            if element is not None:
                patient_data[field] = element.text
                print(f"{field}: {element.text}")
        
        return patient_data if patient_data else None
    except ET.ParseError as e:
        print(f"Error parsing XML for SEARCH_PATIENT: {str(e)}")
        return None
