import json
from urllib.request import urlopen
from urllib.parse import quote,unquote
import time
import unicodedata
def dec2utf8(resp):
    decoded = ''
    for line in resp:
        decoded += line.decode('utf-8')
    return decoded
def convert(str1):
    l1 = list(str1.split("/"))
    print(l1)
    l2 = []
    l3 = []
    l4 = []
    year = int(l1[0])
    month = int(l1[1])
    day = int(l1[2])
    a = int(1382 / 4)
    b = int(2003 / 4)
    x = (1382 * 365) + (3 * 31) + 13 + 345
    y = (2003 * 365) + 31 + 29 + 31 + 30 + 31 + 30 + 3 + 500
    z = y - x
    if 1 <= month - 1 and month - 1 <= 6:
        c = (year - 1) * 365 + (month - 1) * 31 + day + a
        c += z
        c -= b
        newyear = int(c / 365 + 1)
        d = c % 365
    elif month - 1 >= 7 and month - 1 <= 12:
        c = (year - 1) * 365 + (month - 1) * 30 + day + a
        c += z
        c -= b
        newyear = int(c / 365 + 1)
        d = c % 365
    for i in range(1900,2021,4):
        l2.append(i)
    l3.append(31)
    l3.append(28)
    l3.append(31)
    l3.append(30)
    l3.append(31)
    l3.append(30)
    l3.append(31)
    l3.append(31)
    l3.append(30)
    l3.append(31)
    l3.append(30)
    l3.append(31)
    if newyear in l2:
        j = 0
        l3[1] = 29
        while d >= 32:
            d -= l3[j]
            j += 1
        newmonth = j + 1
        newday = d
    else:
        k = 0
        while d >= 32:
            d -= l3[k]
            k += 1
        newmonth = k + 1
        newday = d
    l4.append(str(newyear))
    l4.append(str(newmonth))
    l4.append(str(newday))
    str2 = ''
    str2 = "/".join(l4)
    return str2
TOKEN = '1179463628:AAGCg_Q0CRziL76dHsTc6kEHLLSLuPScVdA'
URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)
cmd = 'getme'
resp = urlopen(URL + cmd)
line = dec2utf8(resp)
gtm = json.loads(line)
status = True
while status:
    cmd = 'getUpdates'
    resp = urlopen(URL + cmd)
    line = dec2utf8(resp)
    upds = json.loads(line)
    NoM = len(upds['result'])
    chck = json.loads(line)

    if NoM != 0:
        msg = upds['result'][0]['message']
        chid = str(msg['chat']['id'])

        if 'text' in msg:
            if quote(msg['text'].encode('utf-8')) != '/start':
                str1 = convert(quote(msg['text'].encode('utf-8')))
                txt = quote(str1.encode('utf-8'))
            else:
                txt = quote('koft'.encode('utf-8'))
            cmd = 'sendMessage'
            resp = urlopen(URL + cmd + '?chat_id={}&text={}'.format(chid, txt))
            line = dec2utf8(resp)
            chck = json.loads(line)

            if chck['ok']:
                uid = upds['result'][0]['update_id']
                cmd = 'getUpdates'
                urlopen(URL + cmd + '?offset={}'.format(uid + 1))
        elif 'digit' in msg:
            digit1 = quote(msg['digit'].encode('utf-8'))
        else:
            uid = upds['result'][0]['update_id']
            cmd = 'getUpdates'
            urlopen(URL + cmd + '?offset={}'.format(uid + 1))
    print('waiting!')
    time.sleep(2)
