import os
import json

def _ensure_cache_dir(cache_dir):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

def _get_cache_file(cache_dir, filename):
    return os.path.join(cache_dir, filename)

def save_xml_response_table2(patient_id, xml_text):
    cache_dir = "container_xml_table2"
    _ensure_cache_dir(cache_dir)
    cache_file = _get_cache_file(cache_dir, f"patient_{patient_id}.xml")
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(xml_text)
    except Exception as e:
        print(f"Error saving XML response for patient {patient_id}: {str(e)}")

def save_xml_response_table3(encounter_id, xml_text):
    cache_dir = "container_xml_table3"
    _ensure_cache_dir(cache_dir)
    cache_file = _get_cache_file(cache_dir, f"encounter_{encounter_id}.xml")
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(xml_text)
    except Exception as e:
        print(f"Error saving XML response for encounter {encounter_id}: {str(e)}")

def load_xml_response_table2(patient_id):
    cache_file = _get_cache_file("container_xml_table2", f"patient_{patient_id}.xml")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error loading XML response for patient {patient_id}: {str(e)}")
    return None

def load_xml_response_table3(encounter_id):
    cache_file = _get_cache_file("container_xml_table3", f"encounter_{encounter_id}.xml")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error loading XML response for encounter {encounter_id}: {str(e)}")
    return None

def save_json_response_table6(encounter_id, json_data):
    cache_dir = "container_json_table6"
    _ensure_cache_dir(cache_dir)
    cache_file = _get_cache_file(cache_dir, f"labs_{encounter_id}.json")
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            if isinstance(json_data, str):
                f.write(json_data)
            else:
                json.dump(json_data, f, indent=2)
    except Exception as e:
        print(f"Error saving JSON response for encounter {encounter_id}: {str(e)}")

def load_json_response_table6(encounter_id):
    cache_file = _get_cache_file("container_json_table6", f"labs_{encounter_id}.json")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON response for encounter {encounter_id}: {str(e)}")
    return None

