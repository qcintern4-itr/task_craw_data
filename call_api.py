import requests
from read_csv import read_last_values
import time
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import json
from config import API_URL, API_PARAMS, API_HEADERS, XML_FIELD_MAPPINGS

def transform_value(field, value):
    if value is None:
        return ""
    if field == 'chart_lock_status':
        return "Locked" if value == "1" else "Unlocked"
    if field == 'unnbilled':
        return "FALSE" if value == "1" else "TRUE"
    if field == 'encounterdate':
        try:
            # Chuyển từ YYYY-MM-DD sang DD/MM/YYYY
            date_obj = datetime.strptime(value, "%Y-%m-%d")
            return date_obj.strftime("%d/%m/%Y")
        except:
            return value
    return value

def extract_xml_values(xml_text):
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

def save_xml_response(patient_id, xml_text):
    cache_dir = "container_xml"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    cache_file = os.path.join(cache_dir, f"patient_{patient_id}.xml")
    with open(cache_file, "w", encoding="utf-8") as f:
        f.write(xml_text)

def load_xml_response(patient_id):
    cache_file = os.path.join("container_xml", f"patient_{patient_id}.xml")
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read()
    return None

def call_api_with_patient_id(patient_id, use_cache=True):
    if use_cache:
        cached_response = load_xml_response(patient_id)
        if cached_response:
            print(f"Using cached data for patient {patient_id}")
            patient_data = extract_xml_values(cached_response)
            if patient_data:
                print(patient_data)
            return patient_data

    # Update dynamic parameters
    params = API_PARAMS.copy()
    params.update({
        "PatientId": patient_id,
        # "rnd2": str(time.time()),
        # "timestamp": str(int(time.time() * 1000))
    })

    try:
        response = requests.get(API_URL, headers=API_HEADERS, params=params)
        
        if response.status_code == 200:
            # Save response to cache
            save_xml_response(patient_id, response.text)
            
            # Extract values from XML response
            patient_data = extract_xml_values(response.text)
            if patient_data:
                print(patient_data)
            return patient_data
        else:
            print(f"Failed to fetch data for patient {patient_id}: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error occurred for patient {patient_id}: {str(e)}")
        return None