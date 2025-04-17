import json
from datetime import datetime, timedelta

# Base URLs
BASE_URL = "https://nymegrapp.eclinicalweb.com/mobiledoc/jsp"
API_URLS = {
    'DETAIL_ENCOUNTER': f"{BASE_URL}/catalog/xml/getPtEncounters.jsp",
    'DETAIL_LOG': f"{BASE_URL}/catalog/xml/getLogs.jsp",
    'DELETE_ENCOUNTER': f"{BASE_URL}/catalog/xml/getPtEncounters.jsp",
    'DETAIL_LAB': f"{BASE_URL}/webemr/labs/LabsRequestHandler.jsp",
    'PATIENT_SEARCH': f"{BASE_URL}/catalog/xml/getPatients.jsp"
}

# Common Configuration
COMMON_CONFIG = {
    'sessionDID': "44972",
    'TrUserId': "44972",
    'Device': "webemr",
    'clientTimezone': "Etc/GMT+8"
}

# Common Parameters
COMMON_PARAMS = {
    "FacilityId": "0",
    "LogView": "true",
    "ProviderId": "0",
    "UnlockedEnc": "0",
    "fromDate": None,
    "toDate": None,
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
    "sessionDID": COMMON_CONFIG['sessionDID'],
    "TrUserId": COMMON_CONFIG['TrUserId'],
    "Device": COMMON_CONFIG['Device'],
    "ecwappprocessid": "0",
    "rnd2": None,
    "timestamp": None,
    "clientTimezone": COMMON_CONFIG['clientTimezone'],
}

# API Parameters
API_PARAMS = {
    'DETAIL_ENCOUNTER': {
        **COMMON_PARAMS,
        "PatientId": None,
        "EncOptions": "0",
        "DelOptions": "0",
        "callingfor": "PATIENT_HUB_ENCOUNTER_LOOKUP",
        "IncludeEncCount": "1"
    },
    'DETAIL_LOG': {
        **COMMON_PARAMS,
        "EncounterId": None
    },
    'DELETE_ENCOUNTER': {
        **COMMON_PARAMS,
        "PatientId": None,
        "EncOptions": "0",
        "DelOptions": "1",
        "callingfor": "PATIENT_HUB_ENCOUNTER_LOOKUP",
        "IncludeEncCount": "1"
    },
    'DETAIL_LAB': {
        **COMMON_PARAMS,
        "pd": "7c9829ab22ea913aea64dec379be8d2e989aebf75294ece60ebe0c1591429775"
    },
    'PATIENT_SEARCH': {
        "sessionDID": "44972",
        "TrUserId": "44972",
        "Device": "webemr",
        "ecwappprocessid": "0",
        "rnd2": "0.2686293953139125",
        "timestamp": "1744846931434",
        "clientTimezone": "Etc/GMT+8",
        "pd": "13e71cf0c19329cd4893d0d5cb66f0a1ed6e82cd04e2f4949e5f1d7d6b7fc9c2"
    }
}


QUICK_SEARCH_FILTER = {
# Form Data for DETAIL_LAB
    "sContext": "PNscreen",
    "qsMarginTop": -2,
    "nPatientId": None,
    "nTrUserId": COMMON_CONFIG['TrUserId'],
    "nEncounterId": None,
    "nDoctorId": None,
    "nDxItemId": 0,
    "sActionType": ""
}

# Form Data
FORM_DATA = {
    'DETAIL_LAB': {
        "QuickSearchFilterObj": json.dumps(QUICK_SEARCH_FILTER),
        "sRequestFrom": "qsDirective",
        "sRequestType": "loadQuickSearchData"
    },
    'PATIENT_SEARCH': {
        "counter": "1",
        "AccountNo": None,
        "primarySearchValue": None,
        "StatusSearch": "Active",
        "enc": "0",
        "limitstart": "0",
        "limitrange": "15",
        "AddlSearchBy": "DateOfBirth",
        "MAXCOUNT": "15",
        "column1": "AllPhones",
        "column2": "GrName",
        "column3": "LastAppt",
        "primarySearchValue": None,
        "device": "webemr",
        "callFromScreen": "PatientSearch",
        "action": "Patient",
        "SearchBy": "AccountNo",    
    }
}


# Request Headers
API_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "X-CSRF-Token": "5044b8b9-764d-45c6-852b-a81fb7cb6145",
    "Referer": f"{BASE_URL}/webemr/index.jsp",
    "Origin": "https://nymegrapp.eclinicalweb.com",
    "Cookie": "JSESSIONID=25E89F737BE9B294EAF1887EAB3AA415; ApplicationGatewayAffinityCORS=124274af792cba06a0461a764f502f20; ApplicationGatewayAffinity=124274af792cba06a0461a764f502f20"
}

# Field Mappings
ENCOUNTER_FIELD_MAPPINGS = {
    'id': 'encounterID',
    # 'patientid': 'patientID',
    'patientid': 'id',
    'acc_no': '',
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

# Export specific constants for backward compatibility
API_URL_DETAIL_ENCOUNTER = API_URLS['DETAIL_ENCOUNTER']
API_URL_DETAIL_LOG = API_URLS['DETAIL_LOG']
API_URL_DELETE_ENCOUNTER = API_URLS['DELETE_ENCOUNTER']
API_URL_DETAIL_LAB = API_URLS['DETAIL_LAB']
API_URL_PATIENT_SEARCH = API_URLS['PATIENT_SEARCH']

API_PARAMS_DETAIL_ENCOUNTER = API_PARAMS['DETAIL_ENCOUNTER']
API_PARAMS_DETAIL_LOG = API_PARAMS['DETAIL_LOG']
API_PARAMS_DELETE_ENCOUNTER = API_PARAMS['DELETE_ENCOUNTER']
API_PARAMS_DETAIL_LAB = API_PARAMS['DETAIL_LAB']
API_PARAMS_PATIENT_SEARCH = API_PARAMS['PATIENT_SEARCH']

FORM_DATA_DETAIL_LAB = FORM_DATA['DETAIL_LAB']
FORM_DATA_PATIENT_SEARCH = FORM_DATA['PATIENT_SEARCH']
QuickSearchFilterObj = QUICK_SEARCH_FILTER