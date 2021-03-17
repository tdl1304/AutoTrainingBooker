import json
from datetime import datetime
from datetime import timedelta
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

global time
global token
# setup
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


#  get token for session
def setToken():
    global token
    response = requests.get(url=request['treneselv']['url'], data=None, headers=header)
    if response.status_code == 200:
        for lines in response.iter_lines():
            if b'token:' in lines:
                string = str(lines, 'UTF-8').strip()
                startIndex = string.find('"') + 1
                endIndex = string.rfind('"')
                token = string[startIndex:endIndex]
                break
    else:
        print('Response code for token:', response.status_code)
        input("press close to exit")
        exit(-1)


# set cookies
def setCookie(email, password):
    try:
        response = requests.post(url=request['login']['url'],
                                 data={"name": email, "pass": password, "op": "Logg inn", "form_id": "user_login"},
                                 headers=header)
        if response.status_code == 200:
            header['Cookie'] = response.request.headers['Cookie']
        elif response.status_code >= 500:
            print("Internal server errors")
            print("Trying again in an hour")
            tm.sleep(3600)
            setCookie(email, password)
        else:
            print('Response code for cookie:', response.status_code)
            input("press close to exit")
            exit(-1)
    except KeyError:
        print('Username and password is wrong. Please edit sit.psw file accordingly')
        input("press close to exit")
        exit(-1)


# gets schedule in two days
def getSchedule():
    n = 0
    while n < 20:
        try:
            day = getSecondDay()
            requestURL = request['schedule']['url'] + \
                         '?studios=' + str(studio) + \
                         '&token=' + token
            response = requests.get(url=requestURL, data=None, headers=header)
            if response.status_code == 200:
                res_json = response.json()
                if res_json['days'] is not None:
                    daySchedule = [element for element in res_json['days'] if element['dayName'] == day]
                    class_ = [element for element in daySchedule[0]['classes'] if time in element['from']]
                    return class_[0]
            elif response.status_code == 403:
                setCookie(email=username, password=passwd)
                setToken()
            else:
                n += 1
        except Exception as inst:
            print('Exception with getSchedule occurred', datetime.now().time())
            input("press close to exit")
            exit(type(inst))
    return None


def getSecondDay():
    today_ = datetime.today().weekday()
    secondDay = today_ + 2
    if secondDay > 6:
        secondDay -= 7
    return days[secondDay]


#  Time difference between sessions
#  Default is next day at specified time from user
def deltaDays():
    today_x = datetime.today()
    thatDay = datetime(today_x.year, today_x.month, today_x.day, int(time[:2]), int(time[3:]), 0, 0) + timedelta(days=1)
    now = datetime.now()
    difference = thatDay - now
    return difference.total_seconds()


# Main func
def main():
    setCookie(email=username, password=passwd)
    setToken()
    print(getSchedule())
    bookable = False
    print('Running')
    deltaTime = (datetime(datetime.today().year, datetime.today().month, datetime.today().day, int(time[:2]),
                          int(time[3:]),
                          0, 0) - datetime.now()).total_seconds()
    if deltaTime < 6:
        print('Auto Training Booker ran too late, skipping 1 day')
        bookable = True
    else:
        print('Waiting for queue to open', deltaTime - 5)
        tm.sleep(deltaTime - 5)
    while True:
        while not bookable:
            class_select = getSchedule()
            if class_select is None:
                print("Tried to send 20 requests to server with no success, skipping a day")
                bookable = True
            elif class_select['bookable']:
                res = requests.post(url=request['book']['url'],
                                    data={"classId": class_select['id'], "token": token},
                                    headers=header)
                if res.status_code == 200:
                    print('Booked for', class_select['from'])
                    bookable = True
                elif res.json()['errorCode'] == 1005:
                    print("Already booked", class_select['from'])
                    bookable = True
                elif res.json()['errorCode'] == 1013:
                    print("You have overlapping bookings, fix this manually and rerun")
                    input("press close to exit")
                    exit(-1)
                else:
                    print("Something unexpected happened")
                    input("press close to exit")
                    exit(-1)
            elif datetime.now().hour == int(time[:2]) and datetime.now().min > int(time[3:]):
                print("Too many retries, waiting for next day")
                bookable = True
            else:
                print('waiting for queue to open', datetime.now().time())
                tm.sleep(5)  # check every 5 sec
        try:
            print('Waiting till the next day totalsecs:', deltaDays() - 5)
            tm.sleep(deltaDays() - 5)  # waits till the next day 5 seconds before
            bookable = False
        except Exception as e:
            print(type(e))
            print(e)


if __name__ == '__main__':
    main()
