import os

def save_xml_response_table2(patient_id, xml_text):
    cache_dir = "container_xml_table2"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    cache_file = os.path.join(cache_dir, f"patient_{patient_id}.xml")
    with open(cache_file, "w", encoding="utf-8") as f:
        f.write(xml_text)

def save_xml_response_table3(encounter_id, xml_text):
    cache_dir = "container_xml_table3"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    cache_file = os.path.join(cache_dir, f"encounter_{encounter_id}.xml")
    with open(cache_file, "w", encoding="utf-8") as f:
        f.write(xml_text)

def load_xml_response_table2(patient_id):
    cache_file = os.path.join("container_xml_table2", f"patient_{patient_id}.xml")
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read()
    return None

def load_xml_response_table3(encounter_id):
    cache_file = os.path.join("container_xml_table3", f"encounter_{encounter_id}.xml")
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read()
    return None

def save_json_response_table6(encounter_id, json_text):
    cache_dir = "container_json_table6"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    cache_file = os.path.join(cache_dir, f"labs_{encounter_id}.json")
    with open(cache_file, "w", encoding="utf-8") as f:
        f.write(json_text)

def load_json_response_table6(encounter_id):
    cache_file = os.path.join("container_json_table6", f"labs_{encounter_id}.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read()
    return None

