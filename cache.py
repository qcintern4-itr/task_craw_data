import os
import json
from typing import Optional

CACHE_DIR = "cache"

def ensure_cache_dir():
    """Ensure cache directory exists."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def save_xml_response_detail_encounter(patient_id: str, response_text: str) -> None:
    """Save XML response for DETAIL_ENCOUNTER."""
    ensure_cache_dir()
    filename = os.path.join(CACHE_DIR, f"detail_encounter_{patient_id}.xml")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response_text)

def load_xml_response_detail_encounter(patient_id: str) -> Optional[str]:
    """Load cached XML response for DETAIL_ENCOUNTER."""
    filename = os.path.join(CACHE_DIR, f"detail_encounter_{patient_id}.xml")
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def save_xml_response_detail_log(encounter_id: str, response_text: str) -> None:
    """Save XML response for DETAIL_LOG."""
    ensure_cache_dir()
    filename = os.path.join(CACHE_DIR, f"detail_log_{encounter_id}.xml")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response_text)

def load_xml_response_detail_log(encounter_id: str) -> Optional[str]:
    """Load cached XML response for DETAIL_LOG."""
    filename = os.path.join(CACHE_DIR, f"detail_log_{encounter_id}.xml")
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def save_json_response_detail_lab(patient_id: str, response_data: dict) -> None:
    """Save JSON response for DETAIL_LAB."""
    ensure_cache_dir()
    filename = os.path.join(CACHE_DIR, f"detail_lab_{patient_id}.json")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(response_data, f, indent=2)

def load_json_response_detail_lab(patient_id: str) -> Optional[dict]:
    """Load cached JSON response for DETAIL_LAB."""
    filename = os.path.join(CACHE_DIR, f"detail_lab_{patient_id}.json")
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_xml_response_search_patient(acc_no: str, response_text: str) -> None:
    """Save XML response for SEARCH_PATIENT."""
    ensure_cache_dir()
    filename = os.path.join(CACHE_DIR, f"search_patient_{acc_no}.xml")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response_text)

def load_xml_response_search_patient(acc_no: str) -> Optional[str]:
    """Load cached XML response for SEARCH_PATIENT."""
    filename = os.path.join(CACHE_DIR, f"search_patient_{acc_no}.xml")
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    return None
