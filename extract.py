import xml.etree.ElementTree as ET
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