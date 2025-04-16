import requests

url = "https://nymegrapp.eclinicalweb.com/mobiledoc/jsp/webemr/labs/LabsRequestHandler.jsp"

params = {
    "sessionDID": "44972",
    "TrUserId": "44972",
    "Device": "webemr",
    "ecwappprocessid": "0",
    "rnd2": "0.29205392363868965",
    "timestamp": "1744752667280",
    "clientTimezone": "Etc/GMT+8",
    "pd": "7c9829ab22ea913aea64dec379be8d2e989aebf75294ece60ebe0c1591429775"
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "X-CSRF-TOKEN": "8ecad037-aef6-45d6-b555-5dc62bbf3702",
    "Origin": "https://nymegrapp.eclinicalweb.com",
    "Referer": "https://nymegrapp.eclinicalweb.com/mobiledoc/jsp/webemr/index.jsp",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "isajaxrequest": "true",
    "Cookie": "JSESSIONID=10FD4EF51079E810A51B0E262E445386; ApplicationGatewayAffinityCORS=9e5222c990b36c49735ac826c4a5b51b; ApplicationGatewayAffinity=9e5222c990b36c49735ac826c4a5b51b"
}

data = {
    "QuickSearchFilterObj": '{"sContext":"PNscreen","qsMarginTop":-2,"nPatientId":"110508","nTrUserId":"44972","nEncounterId":"2378385","nDoctorId":"66194","nDxItemId":0,"sActionType":""}',
    "sRequestFrom": "qsDirective",
    "sRequestType": "loadQuickSearchData"
}

response = requests.post(url, params=params, data=data, headers=headers)

# Kiểm tra phản hồi
print("Status code:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
try:
    print("JSON response:", response.json())
except ValueError:
    print("Không phải JSON, đây là text trả về:")
    # print(response.text)
