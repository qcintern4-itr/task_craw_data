from datetime import datetime

def transform_value(field, value):
    if value is None:
        return ""
    if field == 'chart_lock_status':
        return "Locked" if value == "1" else "Unlocked"
    if field == 'unnbilled':
        return "FALSE" if value == "1" else "TRUE"
    if field in ['encounterdate', 'createdate']:
        try:
            date_obj = datetime.strptime(value, "%Y-%m-%d")
            return date_obj.strftime("%d/%m/%Y")
        except:
            return value
    return value 