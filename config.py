# API Configuration
API_URL = "https://nymegrapp.eclinicalweb.com/mobiledoc/jsp/catalog/xml/getPtEncounters.jsp"

# API Parameters
API_PARAMS = {
    "PatientId": None,  # Will be set dynamically
    "FacilityId": "0",
    "LogView": "true",
    "EncOptions": "0",
    "DelOptions": "0",
    "ProviderId": "0",
    "UnlockedEnc": "0",
    "fromDate": "4/1/2025",
    "toDate": "4/1/2025",
    "ICDItemId": "0",
    "strDeviceType": "webemr",
    "CaseId": "0",
    "CaseTypeId": "0",
    "ecwVisitStatusFlag": "true",
    "blockedEncounterFlagRequest": "true",
    "includeConfidentialInfo": "true",
    "excludeBlockedEncounter": "false",
    "counter": "0",
    "MAXCOUNT": "50",
    "callingfor": "PATIENT_HUB_ENCOUNTER_LOOKUP",
    "IncludeEncCount": "1",
    "sessionDID": "44972",
    "TrUserId": "44972",
    "Device": "webemr",
    "ecwappprocessid": "0",
    "rnd2": None,  # Will be set dynamically
    "timestamp": None,  # Will be set dynamically
    "clientTimezone": "Etc/GMT+8"
}

# Request Headers
API_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "X-CSRF-Token": "771f0f6e-4b11-4137-b6f0-864702b11896",
    "Referer": "https://nymegrapp.eclinicalweb.com/mobiledoc/jsp/webemr/index.jsp",
    "Origin": "https://nymegrapp.eclinicalweb.com",
    "Cookie": "JSESSIONID=F2D544C4AD6E11D2BAFC9CDC157FC033; ApplicationGatewayAffinityCORS=124274af792cba06a0461a764f502f20; ApplicationGatewayAffinity=124274af792cba06a0461a764f502f20"
}

# XML field mappings
XML_FIELD_MAPPINGS = {
    'id': 'encounterID',
    'patientid': 'encounterID',
    'physicianid': 'doctorID',
    'practiceid': 'facilityId',
    'facilityname': 'FacName',
    'unnbilled': 'ClaimReq',
    'chart_lock_status': 'encLock',
    'visittype': 'visitType',
    'description': 'visitTypeDetails',
    'encounterdate': 'date',
    'remarks': '',
    'sourceencounterid': 'resourceId',
    'isdeleted': 'blockedEncounter',
    'createdate': '',
    'npi': '',
    'providerfirstname': 'ufname',
    'providerlastname': 'ulname',
    'datasource': '',
    'icd_code_9': '',
    'icd_code_10': '',  
} 