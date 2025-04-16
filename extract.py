import xml.etree.ElementTree as ET
import json
from transform import transform_value
from config import XML_FIELD_MAPPINGS

def extract_xml_values_table2(xml_text):
    try:
        root = ET.fromstring(xml_text)
        data = {}
        for field, xml_tag in XML_FIELD_MAPPINGS.items():
            if not xml_tag: 
                data[field] = ""
                continue
            element = root.find(f'.//{xml_tag}')
            value = element.text if element is not None else ""
            data[field] = transform_value(field, value)
        return data
    except ET.ParseError:
        return None

def extract_encounter_id_from_table2(xml_text):
    try:
        root = ET.fromstring(xml_text)
        encounter_element = root.find('.//encounterID')
        if encounter_element is not None:
            return encounter_element.text
        return None
    except ET.ParseError:
        return None

def extract_xml_values_table3(xml_text):
    try:
        root = ET.fromstring(xml_text)
        data = {}
        # Lấy log đầu tiên
        first_log = root.find('.//log')
        if first_log is not None:
            date_element = first_log.find('.//date')
            if date_element is not None:
                data['createdate'] = transform_value('createdate', date_element.text)
        return data
    except ET.ParseError:
        return None

def extract_json_values_table6(json_text):
    try:
        response_data = json.loads(json_text)
        labs_data = {}
        
        # Get npi from nProviderId
        if 'nProviderId' in response_data:
            labs_data['npi'] = response_data['nProviderId']
            labs_data['npi'] = response_data['nProviderId']
        
        # Get icd_code_10 from DxList
        if 'DxList' in response_data and 'Dx' in response_data['DxList']:
            dx_codes = [dx['dxItemCode'] for dx in response_data['DxList']['Dx']]
            labs_data['icd_code_10'] = ', '.join(dx_codes)
        
        return labs_data
    except json.JSONDecodeError:
        return None

