from datetime import datetime
import json
from os import path
import sys
from .webdriver import driverChrome
from .reservation_steps import *
from .constant import * 

CONFIG_FILE = DATA_PATH / 'config.json'
RESERVATION_TEXT_FILE = ROOT_PATH / 'teetimes_reservation.txt'

def writeFileText(time, state):
    if path.exists(RESERVATION_TEXT_FILE) == False:
        with open(RESERVATION_TEXT_FILE, 'w') as times:
            times.write(f'-{datetime.today()}: Teetimes = {time} -> {state}' + "\n")
    else: 
        with open(RESERVATION_TEXT_FILE, 'a') as times:
            times.write(f'-{datetime.today()}: Teetimes = {time} -> {state}' + "\n")

def read_json(archivo):
    with open(archivo, encoding='utf-8') as archivo_json:
        return json.load(archivo_json)

def main():
    # Read user configuration from the data folder
    configJson = read_json(CONFIG_FILE)
    
    userData = configJson['user']
    teetimesData = configJson['teetimes']

    try:
        # Go to website
        driverChrome.get(WEBSITE_URL)

        # User login on the website
        loginUser(driverChrome, userData['username'], userData['pass'])
        
        # Number of times reserved
        numberOfTeetimes = len(teetimesData['time'])
        
        if (teetimesData['isScheduled']):
            for i in range(numberOfTeetimes):
                timesData=""
                try:
                    print("-------------------------------------------")
                    selectDay(driverChrome, teetimesData['day'])
                    selectTime(driverChrome, teetimesData['time'][i])
                    timesData = getDateTime(driverChrome)
                    print(timesData)
                    selectNumOfPlayers(driverChrome, teetimesData['numOfPlayers'])
                    pressBook(driverChrome)
                    pressReserveTeeTimes(driverChrome)
                    waitSuccessReservation(driverChrome)
                    writeFileText(str(timesData), 'success')
                except Exception as ex:
                    if timesData!='':
                        writeFileText(str(timesData), 'failure')
                    else:
                        writeFileText(str(teetimesData['day']), 'failure')
        else: 
            for i in range(teetimesData['theFirstNTimes']):
                timesData=""
                try:
                    print("-------------------------------------------")
                    selectDay(driverChrome, teetimesData['day'])
                    selectFirstTime(driverChrome)
                    timesData = getDateTime(driverChrome)
                    print(timesData)
                    selectNumOfPlayers(driverChrome, teetimesData['numOfPlayers'])
                    pressBook(driverChrome)
                    pressReserveTeeTimes(driverChrome)
                    waitSuccessReservation(driverChrome)
                    writeFileText(str(timesData), 'success')
                except Exception as ex:
                    clickTeeTimes(driverChrome)
                    if timesData!='':
                        writeFileText(str(timesData), 'failure')
                    else:
                        writeFileText(str(teetimesData['day']), 'failure')

        print("-------------------------------------------")
        driverChrome.quit()
    except Exception as ex:
        print(f'{ex.__class__.__name__}: {ex}')
        driverChrome.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()

