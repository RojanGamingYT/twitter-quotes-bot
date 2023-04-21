import requests
import random , string, time
import os
import binascii
import threading
from colorama import Fore

created = 0

def get_rstr(lenght: int) -> str:
    return str(binascii.b2a_hex(os.urandom(lenght)).decode('utf-8'))

def Gen():  
    global created            
    email    = ''.join(random.choices('poiuytrewqlkjhgfdsamnbvcxz098765431', k=8)) + '@gmail.com'
    headers = {
    'authority': 'api.getwaitlist.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.opus.pro',
    'referer': 'https://www.opus.pro/',
    'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
}
    json_data = {
    'waitlist_id': 5220,
    'referral_link': 'https://www.opus.pro/waitlist?utm_source=waitlist?ref_id=782VN49JP',
    'heartbeat_uuid': '398711bb-6586-47e6-930a-e5950342efec',
    'email'   : email,
    'question_1': "What's your YouTube video link or website?",
    'question_2': 'Which country are you from?',
    'answer_1': 'N/A',
    'answer_2': 'N/A',
} 
    response = requests.post('https://api.getwaitlist.com/api/v1/waiter', headers=headers, json=json_data)
    if response.status_code == 200:
            created +=1
            print(f"{Fore.BLUE}[ {Fore.GREEN}+ {Fore.BLUE}]{Fore.RESET} Generated - ({created})")

os.system('cls')
thread = int(input("threads: "))

if __name__ == '__main__':
    for i in range(thread):
        threading.Thread(target=Gen).start()
#        time.sleep(random.randint(0, 1))
