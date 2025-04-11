import requests
import xml.etree.ElementTree as ET
import csv
from config import API_URL, API_PARAMS, HEADERS

def extract_encounter_data(xml_text):
    try:
        # Parse XML string
        root = ET.fromstring(xml_text)
        
        # Find encounter and patient elements
        encounter = root.find(".//encounter")
        patient = root.find(".//patient")
        
        if encounter is None or patient is None:
            raise ValueError("Could not find encounter or patient data in XML")
            
        # Extract data with XML tags
        fields = {
            'chart_lock_status': 'encLock',
            'description': 'visitType',
            'encounterdate': 'date',
            'id': 'encounterId',
            'patientid': 'patientId',
            'remarks': 'reason',
            'sourceencounterid': 'ResourceId'
        }
        
        data = []
        for field, xml_tag in fields.items():
            element = encounter.find(xml_tag)
            value = element.text if element is not None else ''
            xml_component = f"<{xml_tag}>{value}</{xml_tag}>"
            
            row = {
                'field': field,
                'meaning': '', 
                'key_component': xml_component,
                'value': value,
                'rule': '',  
                'note': ''   
            }
            data.append(row)
            
        return data
    except ET.ParseError as e:
        print(f"Error parsing XML: {str(e)}")
        return None
    except Exception as e:
        print(f"Error extracting data: {str(e)}")
        return None

def fetch_encounter_data():
    try:
        response = requests.get(API_URL, headers=HEADERS, params=API_PARAMS)
        print(response.text)
        
        if response.status_code == 200:
            # Save raw XML response
            # with open("encounter_data.txt", "w", encoding="utf-8") as f:
            #     f.write(response.text)
            # print("Raw data saved to encounter_data.txt")
            
            # Extract and save to CSV
            data = extract_encounter_data(response.text)
            if data:
                # Define CSV headers
                headers = ['field', 'meaning', 'key/component_from_api_response', 'sample_value', 'rule', 'note']
                
                # Write to CSV
                with open('encounter_data.csv', 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(data)
                print("Data saved to encounter_data.csv")
            else:
                print("Failed to extract data from XML response")
        else:
            print(f"Error: {response.status_code}")
          
            
    except Exception as e:
        print(f"Error when performing request: {str(e)}")
