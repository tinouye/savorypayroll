import datetime as dt
import requests
import json

def get_raw_data(start_date, end_date):
    body = build_body(start_date, end_date)
    req = api_call(body)

    request_json = json.loads(req.content)
    print(f"Done: {len(request_json)} rows found.")
    return request_json


def api_call(body):
    with open("code/credentials.txt", mode='r') as credentials_file:
        credentials = credentials_file.readline()
    auth = {"Authorization": f"Bearer {credentials}"}
    url = "https://e57ba010061839.na.deputy.com/api/v1/resource/Timesheet/QUERY"
    
    return requests.post(url, headers=auth, json=body)


def build_body(start_date, end_date):
    start_date = start_date.isoformat()
    end_date = end_date.isoformat()

    return {
        "search": {
            "s1": {
                "field": "Date",
                "data": start_date,
                "type": "ge"
            },
            "s2": {
                "field": "Date",
                "data": end_date,
                "type": "le"
            }
        },
        "join": ["EmployeeObject", "LeaveRuleObject"],
        "sort": {"Employee":"asc", "Date":"asc"}
    }