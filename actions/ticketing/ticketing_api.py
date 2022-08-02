import requests


def get_access_token():
    req_body = {
        "user_id": "chat.bot",
        "password": "sa"
    }
    response = requests.post("https://ticketing.celloscope.net/api/v1/user/signin", json=req_body)
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
        "https://ticketing.celloscope.net/api/v1/save-issue", 
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
        "https://ticketing.celloscope.net/api/v1/issue-list", 
        json=req_body,
        headers= headers
    )

    json_response = response.json() 

    return json_response


if __name__ == "__main__":
    print(create_issue(
        mobile_number="01927040075",
        issuer_name_bn="হুমায়ুন কবির",
        issuer_name_en= "Humayun Kabir",
        address="Munshiganj",
        email="kabir.humayun@doer.com.bd",
        issue_category_oid="ISSUE-OID-0003",
        description="For testing",
        issuer_oid="ISSUER-OID-0001"
    ))

    print(get_issue_list())