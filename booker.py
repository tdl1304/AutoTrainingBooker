import json
from datetime import datetime
import time as tm
import requests
from pathlib import Path

# Auto Booker for sit trondheim treningssentre
# This books an appointment two days ahead accordingly to set time.

sit = "https://www.sit.no/"
ibooking = "https://ibooking.sit.no/webapp/api//Schedule/"
studios = {'Gløshaugen': 306, 'Dragvoll': 307, 'Portalen': 308, 'DMMH': 402, 'Moholt': 540}
request = {
    'treneselv': {'url': sit + 'trening/treneselv', 'method': 'GET'},
    'login': {'url': sit, 'method': 'POST'},
    'book': {'url': ibooking + 'addBooking', 'method': 'POST'},
    'schedule': {'url': ibooking + 'getSchedule', 'method': 'GET'},
}

days = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag', 'Søndag']

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'Connection': 'keep-alive'
}


#  get token for session
def setToken():
    global token
    res = requests.get(url=request['treneselv']['url'], data=None, headers=header)
    for lines in res.iter_lines():
        if b'token:' in lines:
            string = str(lines, 'UTF-8').strip()
            startIndex = string.find('"') + 1
            endIndex = string.rfind('"')
            token = string[startIndex:endIndex]
            break


# set cookies
def setCookie(email, password):
    try:
        res = requests.post(url=request['login']['url'],
                            data={"name": email, "pass": password, "op": "Logg inn", "form_id": "user_login"},
                            headers=header)
        header['Cookie'] = res.request.headers['Cookie']
    except KeyError:
        print('Username and password is wrong. Please edit sit.psw file accordingly')
        input("press close to exit")
        exit(-1)


# gets schedule in two days
def getSchedule():
    try:
        day = getSecondDay()
        requestURL = request['schedule']['url'] + \
                     '?studios=' + str(studio) + \
                     '&token=' + token
        res = requests.get(url=requestURL, data=None, headers=header)
        if res.status_code == 200:
            res_json = res.json()
            if res_json['days'] is not None:
                daySchedule = [element for element in res_json['days'] if element['dayName'] == day]
                class_ = [element for element in daySchedule[0]['classes'] if time in element['from']]
                return class_[0]
        # else this happens
        setCookie(email=username, password=passwd)
        setToken()
        return getSchedule()
    except Exception as inst:
        print('Exception with getSchedule occurred', datetime.now().time())
        input("press close to exit")
        exit(type(inst))


def getSecondDay():
    today = datetime.today().weekday()
    secondDay = today + 2
    if secondDay > 6:
        secondDay -= 7
    return days[secondDay]


if Path("sit.psw").is_file():
    with open('sit.psw') as data_file:
        data_loaded = json.load(data_file)
        username = data_loaded["email"]
        passwd = data_loaded["password"]
    print("Username and password loaded from sit.psw")
else:
    username = input("Username: ")
    passwd = input("Password: ")
    if input("Do you want to save the username and password? WARNING SAVED IN CLEAR TEXT!  (y/n)") == "y":
        with open('sit.psw', 'w') as outfile:
            json.dump({"email": username, "password": passwd}, outfile)
            print("Username and passwd saved to qs.psw")

if Path("config.json").is_file():
    with open('config.json') as inFile:
        data = json.load(inFile)
        studio = data['studio']
        time = data['bookTime']
        print('Settings loaded from config.json')
else:
    print('Velg en av disse:', studios.__str__())
    studio = input('Id on training centre format(integer): ')
    time = input('Preferred booking time format(HH:MM): ')
    with open('config.json', 'w') as out:
        json.dump({
            "studio": int(studio),
            "bookTime": time
        }, out)
    print("Settings saved")

# Main func
setCookie(email=username, password=passwd)
setToken()
bookable = True
lastBooked = datetime.today().weekday()-1
while True:
    today = datetime.today().weekday()  # 0-6
    hour = datetime.now().hour
    while not bookable:
        class_select = getSchedule()
        if class_select['bookable']:
            res = requests.post(url=request['book']['url'],
                                data={"classId": class_select['id'], "token": token},
                                headers=header)
            if res.status_code == 200:
                print('Booked for', class_select['from'])
                lastBooked = today
                bookable = True
            elif res.json()['errorCode'] == 1005:
                print("Already booked", class_select['from'])
                lastBooked = today
                bookable = True
            elif res.json()['errorCode'] == 1013:
                print("You have overlapping bookings, fix this manually and rerun")
                input("press close to exit")
                exit(-1)
            else:
                print("Something unexpected happened")
                input("press close to exit")
                exit(-1)
        else:
            print('waiting for queue to open', datetime.now().time())
            tm.sleep(120)  # check every 120 sec
    # checks for a new day
    if today == lastBooked + 1 and hour == int(time[:2]) - 1:
        bookable = False
    else:
        tm.sleep(3600)  # check every hour
