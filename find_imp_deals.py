"""Find all the important deals happened today."""

import re
import os
import json

import yagmail

from pytz import timezone 
from datetime import datetime

ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y')

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def send_mail(email, data):
    SENDER = os.getenv('SENDER')
    PASS = os.getenv('PASS')

    subject  = 'Important Bulk Deals {}'.format(ind_time)
    content = [ data ]
    with yagmail.SMTP(SENDER, PASS) as yag:
        yag.send(email, subject, content)
        print('{}Sent email successfully{}'.format(GREEN, RESET))

def find_imp_deals():
    TO = os.getenv('TO').split(',')
    try:
        with open('emails.txt', 'r') as emails:
            TO = emails.read().split('\n')
            TO.pop()
    except Exception as e:
        print('{}Exception occured while opening emails.txt {}\n{}'.format(RED, RESET, e))

    details = imp_stk = None
    try:
        with open('bulk_deals', 'r') as bd:
            details = bd.read()

        with open('imp_stk.json', 'r') as istk:
            imp_stk = json.load(istk)

    except Exception as e:
        print('{}Exception occured while opening bulk_deals file{}\n{}'.format(RED, RESET, e))

    if details is not None:
        data = ''
        details_list = details.split('\n')

        find_for = os.getenv('FIND_FOR')
        r = re.compile(r'{}'.format(find_for), flags= re.I | re.X)

        for i in range(0, len(details_list) - 1, 7):
            if r.search(details_list[i + 2]) or imp_stk.get(details_list[i]) :
                data = data + 'Stock: <p style="color:green;display:inline">{}</p>\nClient Name: <p style="color:red;display:inline">{}</p>\nStatus: {}\nQuantity: {}\nAvg. Price: {}\n-\n'.format(details_list[i + 1],
                        details_list[i + 2],
                        details_list[i + 3],
                        details_list[i + 4],
                        details_list[i + 5])
        print(data)
        if data:
            for email in TO:
                send_mail(email, data)

find_imp_deals()

