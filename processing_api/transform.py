from datetime import datetime

TRANSFORMATIONS = {
    'chart_lock_status': lambda v: "Locked" if v == "1" else "Unlocked",
    'unnbilled': lambda v: "FALSE" if v == "1" else "TRUE",
    'isdeleted': lambda _: "FALSE",
    'icd_code_10': lambda v: v, 
    'npi': lambda v: str(v) if v is not None else ""  
}

def transform_value(field, value):
    if value is None:
        return ""
        
    # Handle date fields
    if field in ['encounterdate', 'createdate']:
        try:
            date_obj = datetime.strptime(value, "%Y-%m-%d")
            return date_obj.strftime("%d/%m/%Y")
        except:
            print(f"Error transforming date value: {value}")
            return value
            
    # Handle other transformations
    if field in TRANSFORMATIONS:
        return TRANSFORMATIONS[field](value)
        
    return value