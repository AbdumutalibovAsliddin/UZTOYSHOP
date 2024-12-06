import random
import requests
import re
import json

def send_sms_verification(phone_number,message):
    if phone_number.startswith("998"):
        phone_number = phone_number[3:]  # Telefon raqamini formatlash
    data = {
        'send': '',
        'number': phone_number,
        'text': message,
        'token': 'JLqrMBRsoYmFgxfDSkOvbaZtXQAnyVEUpPiHKGdhlNejuIT',
        'id': 1322,
        'user_id': 1831969115
    }   

    url = f"https://api.xssh.uz/smsv1/?data={requests.utils.quote(json.dumps(data))}"
    response = requests.post(url)
    javob = response.json()
    return True  # Tasdiqlash kodini qaytarish

