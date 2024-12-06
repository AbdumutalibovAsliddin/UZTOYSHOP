# utils.py
import random
import requests
import re
import json

def format_phone_number(phone_number):
    return re.sub(r'\D', '', phone_number)[3:]  # +998 ni olib tashlaydi
def send_verification_code(phone_number):
    phone_number = format_phone_number(phone_number)  # Telefon raqamini formatlash
    code = str(random.randint(100000, 999999))  # 6 raqamli tasdiqlash kodi
    data = {
        'send': '',
        'number': phone_number,
        'text': f"UzToyShop ga kirish kod: {code}. UNI HECHKIMGA AYTMANG. #{code}",
        'token': 'JLqrMBRsoYmFgxfDSkOvbaZtXQAnyVEUpPiHKGdhlNejuIT',
        'id': 1322,
        'user_id': 1831969115
    }   

    url = f"https://api.xssh.uz/smsv1/?data={requests.utils.quote(json.dumps(data))}"
    response = requests.post(url)
    javob = response.json()
    return code  # Tasdiqlash kodini qaytarish

