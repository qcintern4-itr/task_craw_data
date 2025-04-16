import json
# API Configuration
API_URL_TABLE2 = "https://nymegrapp.eclinicalweb.com/mobiledoc/jsp/catalog/xml/getPtEncounters.jsp"
API_URL_TABLE3 = "https://nymegrapp.eclinicalweb.com/mobiledoc/jsp/catalog/xml/getLogs.jsp"
API_URL_TABLE4 = "https://nymegrapp.eclinicalweb.com/mobiledoc/jsp/catalog/xml/getPtEncounters.jsp"
API_URL_TABLE6 = "https://nymegrapp.eclinicalweb.com/mobiledoc/jsp/webemr/labs/LabsRequestHandler.jsp"

# Common Parameters
COMMON_PARAMS = {
    "FacilityId": "0",
    "LogView": "true",
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
    "sessionDID": "44972",
    "TrUserId": "44972",
    "Device": "webemr",
    "ecwappprocessid": "0",
    "rnd2": None,
    "timestamp": None,
    "clientTimezone": "Etc/GMT+8"
}

# API Parameters
API_PARAMS_TABLE2 = {
    **COMMON_PARAMS,
    "PatientId": None,
    "EncOptions": "0",
    "DelOptions": "1",
    "callingfor": "PATIENT_HUB_ENCOUNTER_LOOKUP",
    "IncludeEncCount": "1"
}

API_PARAMS_TABLE3 = {
    **COMMON_PARAMS,
    "EncounterId": None
}

API_PARAMS_TABLE4 = {
    **COMMON_PARAMS,
    "PatientId": None,
    "EncOptions": "0",
    "DelOptions": "1",
    "callingfor": "PATIENT_HUB_ENCOUNTER_LOOKUP",
    "IncludeEncCount": "1"
}

API_PARAMS_TABLE6 = {
    **COMMON_PARAMS,
    "pd": "7c9829ab22ea913aea64dec379be8d2e989aebf75294ece60ebe0c1591429775"  
}

# Form Data for TABLE6
QuickSearchFilterObj = {
    "sContext": "PNscreen",
    "qsMarginTop": -2,
    "nPatientId": None,
    "nTrUserId": "44972",
    "nEncounterId": None,
    "nDoctorId": None,
    "nDxItemId": 0,
    "sActionType": ""
}

FORM_DATA_TABLE6 = {
    "QuickSearchFilterObj": json.dumps(QuickSearchFilterObj),
    "sRequestFrom": "qsDirective",
    "sRequestType": "loadQuickSearchData"
}

# Request Headers
API_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "X-CSRF-Token": "8ecad037-aef6-45d6-b555-5dc62bbf3702",
    "Referer": "https://nymegrapp.eclinicalweb.com/mobiledoc/jsp/webemr/index.jsp",
    "Origin": "https://nymegrapp.eclinicalweb.com",
    "Cookie": "JSESSIONID=10FD4EF51079E810A51B0E262E445386; ApplicationGatewayAffinityCORS=9e5222c990b36c49735ac826c4a5b51b; ApplicationGatewayAffinity=9e5222c990b36c49735ac826c4a5b51b"
}

# XML field mappings
XML_FIELD_MAPPINGS = {
    'id': 'encounterID',
    'patientid': 'patientID',
    'physicianid': 'doctorID',
    'practiceid': 'facilityId',
    'facilityname': 'FacName',
    'unnbilled': 'ClaimReq',
    'chart_lock_status': 'encLock',
    'visittype': 'visitType',
    'description': 'visitTypeDetails',
    'encounterdate': 'date',
    'remarks': 'reason',
    'sourceencounterid': 'resourceId',
    'isdeleted': 'blockedEncounter',
    'createdate': 'date',
    'npi': 'nProviderId',
    'providerfirstname': 'ufname',
    'providerlastname': 'ulname',
    'icd_code_10': 'dxItemCode'
} 