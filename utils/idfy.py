from backend.celery import app
import os
from dotenv import load_dotenv
import requests
from uuid import uuid4
load_dotenv()


@app.task(bind=True)
def get_idfy_request_id(self, rc_number: str, challan_blacklist_details: bool):
    url = "https://eve.idfy.com/v3/tasks/async/verify_with_source/ind_rc_plus"

    task_id = str(uuid4())
    group_id = str(uuid4())
    api_key = os.getenv('IDFY_KEY')
    account_id = os.getenv('IDFY_ID')
    payload = {
        "task_id": task_id,
        "group_id": group_id,
        "data": {
            "rc_number": rc_number,
            "challan_blacklist_details": challan_blacklist_details
        }
    }

    headers = {
        'api-key': api_key,
        'account-id': account_id,
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    return response.json()['request_id']


@app.task(bind=True)
def get_vehicle_details(self, request_id: str):
    url = "https://eve.idfy.com/v3/tasks?request_id=" + request_id

    api_key = os.getenv('IDFY_KEY')
    account_id = os.getenv('IDFY_ID')
    payload = {}

    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json',
        'account-id': account_id,
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()