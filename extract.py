import xml.etree.ElementTree as ET
import json
from typing import Dict, Optional, Union
from transform import transform_value
from config import FIELD_MAPPINGS

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

def extract_xml_values_table2(xml_text: str) -> Optional[Dict]:
    """Extract values from TABLE2 XML response."""
    root = _parse_xml(xml_text)
    if not root:
        return None

    data = {}
    for field, xml_tag in FIELD_MAPPINGS.items():
        if not xml_tag: 
            data[field] = ""
            continue
        element = root.find(f'.//{xml_tag}')
        value = element.text if element is not None else ""
        data[field] = transform_value(field, value)
    return data

def extract_encounter_id_from_table2(xml_text: str) -> Optional[str]:
    """Extract encounter ID from TABLE2 XML response."""
    root = _parse_xml(xml_text)
    if not root:
        return None

    encounter_element = root.find('.//encounterID')
    return encounter_element.text if encounter_element is not None else None

def extract_xml_values_table3(xml_text: str) -> Optional[Dict]:
    """Extract values from TABLE3 XML response."""
    root = _parse_xml(xml_text)
    if not root:
        return None

    data = {}
    first_log = root.find('.//log')
    if first_log is not None:
        date_element = first_log.find('.//date')
        if date_element is not None:
            data['createdate'] = transform_value('createdate', date_element.text)
    return data

def extract_json_values_table6(json_text: str) -> Optional[Dict]:
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

