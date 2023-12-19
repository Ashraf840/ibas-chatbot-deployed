import json
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import http.client


def get_access_token():
    req_body = {
        "user_id": "chat.bot",
        "password": "sa"
    }
    response = requests.post("https://tms-test.celloscope.net/api/v1/user/signin", json=req_body) #ticketing.celloscope.net
    json_response = response.json()
    access_token = json_response['token']['access_token']

    return access_token

def create_issue(
    mobile_number, 
    issuer_name_bn, 
    issuer_name_en, 
    address, 
    email, 
    issue_category_oid, 
    description, 
    issuer_oid
):
    req_body = {
        "mobileNumber": mobile_number, 
        "issuerNameBn": issuer_name_bn, 
        "issuerNameEn": issuer_name_en, 
        "address": address,
        "email": email,
        "issueCategoryOid": issue_category_oid,
        "description": description,
        "issuerOid": issuer_oid
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_access_token()}"
    }

    response = requests.post(
        "https://tms-test.celloscope.net/api/v1/save-issue",
        json=req_body,
        headers= headers
    )

    json_response = response.json() 

    return json_response


def get_issue_list():
    req_body = {
        "status": "Submitted"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_access_token()}"
    }

    response = requests.post(
        "https://tms-test.celloscope.net/api/v1/issue-list",
        json=req_body,
        headers= headers
    )

    json_response = response.json() 

    return json_response

def get_category_list_by_project_oid(project_oid):
    req_body = {
        "projectOid": project_oid
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_access_token()}"
    }

    response = requests.post(
        "https://tms-test.celloscope.net/api/v1/issue-categories-by-project-oid",
        json=req_body,
        headers= headers
    )

    json_response = response.json() 

    return json_response

def get_project_list():

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_access_token()}"
    }

    response = requests.get(
        "https://tms-test.celloscope.net/api/v1/project-list",
        headers= headers
    )

    json_response = response.json() 

    return json_response


def create_issue_v2(
    mobile_number, 
    issuer_name_bn, 
    issuer_name_en, 
    address, 
    email, 
    issue_category_oid, 
    description, 
    issuer_oid,
    sender_id
):
    req_body = {
        "mobileNumber": mobile_number, 
        "issuerNameBn": issuer_name_bn, 
        "issuerNameEn": issuer_name_en, 
        "address": address,
        "email": email,
        "issueCategoryOid": issue_category_oid,
        "description": description,
        "issuerOid": issuer_oid,
        "senderId": sender_id
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_access_token()}"
    }

    response = requests.post(
        "https://tms-test.celloscope.net/api/v1/save-issue",
        json=req_body,
        headers= headers
    )

    json_response = response.json() 

    return json_response

if __name__ == "__main__":

    print(json.dumps(get_issue_list(), indent=4, ensure_ascii=False))
def get_user_detail():
    response = requests.get(f'http://127.0.0.1:8000/home/api/user-chatbot/socket/5fa6894a-e26b-48bb-82cc-30a73be70755/')
    data = response.json()
    return data

def reqres():
    response = requests.get('http://localhost:3000/api/data')
    data = response.json()
    return data

def issue_text(issue_desc):
    issue_description = issue_desc
    return []

def category_oid(category_oid):
    category_oid_value = category_oid

def redirect_to_cso_chatroom():

    payload = "{\n\t\"user_email\": \"test1@gmail.com\",\n\t\"chatbot_socket_id\": \"{sender_id}\"\n}"

    headers = { 'Content-Type': "application/json" }

    response = requests.post(
        "http://127.0.0.1:8000/home/api/user-chatroom/socket/", payload,
        headers= headers
    )

    json_response = response.json() 

    return json_response