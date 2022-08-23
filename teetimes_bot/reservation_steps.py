from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

def clickTeeTimes(driver):
    teetimesButton = driver.find_element(By.XPATH, f'//a[@id="nav-teetimes-id"]')
    teetimesButton.click()
    sleep(1.5)

def selectTime(driver, selectedTime):
    timesAvailable = WebDriverWait(driver, 5).until(lambda d: d.find_elements(By.XPATH, f'//div[@class="col-md-3 col-sm-4 no-gutter"]'))

    for time in timesAvailable:
        if selectedTime.strip() in time.text:
            buttonBook = time.find_element(By.XPATH, './/button[@class="btn btn-success bookNowClass"]')
            buttonBook.click()
            sleep(1.5)
            return True

    print(f'{selectedTime} is not available.')
    raise Exception('time error')

#select the day inside the div named calendar
def selectDay(driver, selectedDay): 
    try:
        daysAvailable = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.XPATH, f'//li/a[contains(@title, "{selectedDay.strip()}")]'))
        daysAvailable.click()
        sleep(1.5)
    except:
        print(f'{selectedDay} is not available')
        raise Exception('day error')

def selectNumOfPlayers(driver, numOfPlayers):
    try:
        buttonNumOfPlayers = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.XPATH, f'//div[@id="qty_popup_notice"]/a[@qty="{numOfPlayers}"]'))
        #print(driver.find_element(By.XPATH, f'//div[@class="col-lg-3 col-sm-4 no-gutter hidden-xs"]').text)
        buttonNumOfPlayers.click()
        sleep(1.5)
    except:
        print(f'{numOfPlayers} players not available.')
        raise Exception('players error')

def loginUser(driver, emailUser, passwordUser):
    navbarLogin = driver.find_element(By.XPATH, f'//ul/li[@id="dropdown-login-id"]')

    buttonLogin = navbarLogin.find_element(By.XPATH, f'//a[@id="dropdown-login"]')
    buttonLogin.click()

    emailText = navbarLogin.find_element(By.XPATH, f'//input[@id="inputUsername"]')
    emailText.send_keys(emailUser + Keys.TAB)

    passText = navbarLogin.find_element(By.XPATH, f'//input[@id="inputPassword"]')
    passText.send_keys(passwordUser + Keys.ENTER)

def pressBook(driver):
    buttonBook = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.XPATH, f'//input[@id="booking_frm_btn_id"]'))
    buttonBook.click()  
    sleep(1.5)

def pressReserveTeeTimes(driver):
    buttonReserve = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.XPATH, f'//a[@id="checkout_frm_btn_id"]'))
    buttonReserve.click()
    sleep(1.5)

def waitSuccessReservation(driver):
    try:
        alertSuccess = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.XPATH, f'//div[@class="alert alert-success  in"]'))
        print(alertSuccess.text)
        detailsBook = driver.find_element(By.XPATH, f'//div[@class="col-lg-9 no-gutter"]')
        print(detailsBook.text)
        clickTeeTimes(driver)
    except:
        print('Reservation was not successful')
        raise Exception('unsuccessful error')