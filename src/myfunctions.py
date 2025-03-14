import requests
import base64
import json
import os
from datetime import datetime

ENDPOINT =  os.getenv("ENDPOINT")
ADMINPASS =  os.getenv("ADMINPASS")

if os.path.exists("/config.conf"):
    with open("/config.conf", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                if key == "ENDPOINT":
                    ENDPOINT = value
                elif key == "ADMINPASS":
                    ADMINPASS = value

def get_date():
    return datetime.utcnow().isoformat()

def generate_json(date, type_, message):
    return json.dumps({"date": date, "type": type_, "message": message})

def mylog(message):
    print(f"{message}", flush=True)

def is_site_accessible():
    try:
        requests.get(ENDPOINT, timeout=2)
    except requests.RequestException:
        mylog(generate_json(get_date(), "failed", "ENDPOINT unavailable"))
        raise Exception("ENDPOINT unavailable")
    
def utf8_to_utf16be_hex(text):
    return text.encode('utf-16be').hex().upper()

def login():
    encoded_password = base64.b64encode(ADMINPASS.encode()).decode()

    url = f"{ENDPOINT}/goform/goform_set_cmd_process"
    headers = {"Referer": f"{ENDPOINT}/index.html"}
    data = {
        "goformId": "LOGIN",
        "isTest": "false",
        "password": encoded_password
    }

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        result = response.json().get("result")
        if result != "0":
            mylog(generate_json(get_date(), "failed", "login"))
            raise Exception("Login failed")
    else:
        mylog(generate_json(get_date(), "error", "HTTP request failed"))
        raise Exception("HTTP request failed")

def logout():
    url = f"{ENDPOINT}/goform/goform_set_cmd_process"
    headers = {"Referer": f"{ENDPOINT}/index.html"}
    data = {
        "goformId": "LOGOUT",
        "isTest": "false"
    }

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        result = response.json().get("result")
        if result != "success":
            mylog(generate_json(get_date(), "failed", "logout"))
            raise Exception("Logout failed")
    else:
        mylog(generate_json(get_date(), "error", "HTTP request failed"))
        raise Exception("HTTP request failed")

def send_sms(phone_number, message):
    hex_message = utf8_to_utf16be_hex(message)

    phone_numbers = phone_number.split(";") if ";" in phone_number else [phone_number]

    for number in phone_numbers:
        number = number.strip()
        url = f"{ENDPOINT}/goform/goform_set_cmd_process"
        headers = {"Referer": f"{ENDPOINT}/index.html"}
        data = {
            "goformId": "SEND_SMS",
            "Number": number,
            "MessageBody": hex_message,
            "ID": "-1",
            "encode_type": "GSM7_default"
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            result = response.json().get("result")
            if result == "success":
                mylog(generate_json(get_date(), "success", "send message to " + number))
            else:
                mylog(generate_json(get_date(), "failed", "send message"))
                raise Exception("Message sending failed")
        else:
            mylog(generate_json(get_date(), "error", "HTTP request failed"))
            raise Exception("HTTP request failed")